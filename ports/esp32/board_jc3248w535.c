 * 初始化JC3248W535CN开发板的硬件：
 *   - ESP32-S3-WROOM-1
 *   - 320x480 QSPI TFT LCD
 *   - I2C Touch Screen
 *   - I2S Audio (MAX98357A)
 *   - SD Card
 */

#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "driver/i2c.h"
#include "driver/i2s_std.h"
#include "driver/ledc.h"
#include "esp_pm.h"
#include "esp_sleep.h"
#include "esp_vfs_fat.h"
#include "sdmmc_cmd.h"
#include "mp.h"
#include "mpconfigport.h"
#include "py/runtime.h"

// ========== 引脚定义 ==========
#define PIN_NUM_LCD_CS        45
#define PIN_NUM_LCD_SCLK      47
#define PIN_NUM_LCD_D0        21
#define PIN_NUM_LCD_D1        48
#define PIN_NUM_LCD_D2        40
#define PIN_NUM_LCD_D3        39
#define PIN_NUM_LCD_DC        8
#define PIN_NUM_LCD_RST       -1  // No reset pin
#define PIN_NUM_LCD_BL        1
#define PIN_NUM_LCD_TE        38

#define PIN_NUM_TOUCH_SDA     4
#define PIN_NUM_TOUCH_SCL     5
#define PIN_NUM_TOUCH_INT     46

#define PIN_NUM_I2S_BCLK      7
#define PIN_NUM_I2S_LRCLK     6
#define PIN_NUM_I2S_DATA      15

#define PIN_NUM_SD_CLK        12
#define PIN_NUM_SD_CMD        11
#define PIN_NUM_SD_D0         13
#define PIN_NUM_SD_D1         20
#define PIN_NUM_SD_D2         3
#define PIN_NUM_SD_D3         42
#define PIN_NUM_SD_CS         41

// ========== 背光PWM控制 ==========
static const ledc_channel_config_t lcd_backlight_channel = {
    .gpio_num = PIN_NUM_LCD_BL,
    .speed_mode = LEDC_LOW_SPEED_MODE,
    .channel = 0,
    .intr_type = LEDC_INTR_DISABLE,
    .timer_sel = 1,
    .duty = 0,
    .hpoint = 0
};

static const ledc_timer_config_t lcd_backlight_timer = {
    .speed_mode = LEDC_LOW_SPEED_MODE,
    .duty_resolution = LEDC_TIMER_10_BIT,
    .timer_num = 1,
    .freq_hz = 5000,  // 5kHz PWM
    .clk_cfg = LEDC_AUTO_CLK
};

/*
 * 初始化背光PWM
 * 使用LEDC控制LCD背光亮度
 */
static void lcd_backlight_init(void) {
    ESP_ERROR_CHECK(ledc_timer_config(&lcd_backlight_timer));
    ESP_ERROR_CHECK(ledc_channel_config(&lcd_backlight_channel));
    lcd_backlight_on();
}

/*
 * 打开背光
 */
void lcd_backlight_on(void) {
    ledc_set_duty(LEDC_LOW_SPEED_MODE, lcd_backlight_channel.channel, 1023);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, lcd_backlight_channel.channel);
}

/*
 * 关闭背光
 */
void lcd_backlight_off(void) {
    ledc_set_duty(LEDC_LOW_SPEED_MODE, lcd_backlight_channel.channel, 0);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, lcd_backlight_channel.channel);
}

/*
 * 设置背光亮度 (0-100%)
 */
void lcd_backlight_set(int brightness_percent) {
    if (brightness_percent < 0) brightness_percent = 0;
    if (brightness_percent > 100) brightness_percent = 100;
    uint32_t duty = (1023 * brightness_percent) / 100;
    ledc_set_duty(LEDC_LOW_SPEED_MODE, lcd_backlight_channel.channel, duty);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, lcd_backlight_channel.channel);
}

/*
 * 初始化I2S音频 (MAX98357A)
 * MAX98357A通过I2S接收数字音频数据
 * 配置为I2S模式, 48kHz采样率, 16位
 */
static void i2s_audio_init(void) {
    i2s_chan_handle_t tx_handle = NULL;
    
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(PIN_NUM_I2S_BCLK, PIN_NUM_I2S_LRCLK);
    chan_cfg.role = I2S_ROLE_MASTER;
    chan_cfg.dma_desc_num = 6;
    chan_cfg.dma_frame_num = 240;
    
    i2s_driver_install(I2S_NUM_0, &chan_cfg, 0, &tx_handle);
    
    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(48000),
        .slot_cfg = I2S_STD_MSB_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_MONO),
        .gpio_cfg = {
            .bclk = PIN_NUM_I2S_BCLK,
            .ws = PIN_NUM_I2S_LRCLK,
            .data_out = PIN_NUM_I2S_DATA,
            .data_in = I2S_GPIO_UNUSED,
        }
    };
    
    i2s_channel_init_std_mode(tx_handle, &std_cfg);
}

/*
 * 播放音频数据
 */
static void i2s_audio_write(const void *data, size_t len) {
    // 这个函数由mp_renpy_audio.c调用
    // 实际实现在音频模块中
}

/*
 * 初始化I2C总线 (触摸屏)
 */
static void i2c_touch_init(void) {
    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = PIN_NUM_TOUCH_SDA,
        .scl_io_num = PIN_NUM_TOUCH_SCL,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = 400000,
    };
    i2c_param_config(I2C_NUM_0, &conf);
    i2c_driver_install(I2C_NUM_0, I2C_MODE_MASTER, 0, 0, 0);
}

/*
 * 初始化SD卡
 */
static sdmmc_card_t* sdcard_init(void) {
    sdmmc_host_t host = SDMMC_HOST_DEFAULT();
    host.flags = SDMMC_HOST_FLAG_4BIT;
    host.max_freq_khz = SDMMC_FREQ_HIGHSPEED;
    
    sdmmc_slot_config_t slot = {
        .clk = PIN_NUM_SD_CLK,
        .cmd = PIN_NUM_SD_CMD,
        .d0 = PIN_NUM_SD_D0,
        .d1 = PIN_NUM_SD_D1,
        .d2 = PIN_NUM_SD_D2,
        .d3 = PIN_NUM_SD_D3,
        .width = 4,
    };
    
    sdmmc_bus_widths_t width = SDMMC_BUS_WIDTH_4;
    
    esp_vfs_fat_sdmmc_mount_config_t mount_config = {
        .format_if_mount_failed = false,
        .max_files = 5,
        .allocation_unit_size = 16 * 1024
    };
    
    sdmmc_card_t* card = NULL;
    esp_err_t ret = esp_vfs_fat_sdmmc_mount("/sdcard", &host, &slot, &mount_config, &card);
    
    if (ret != ESP_OK) {
        if (ret == ESP_FAIL) {
            printf("Failed to mount SD card filesystem\n");
        } else {
            printf("SD card mount failed: 0x%X\n", ret);
        }
        return NULL;
    }
    
    printf("SD card mounted successfully\n");
    return card;
}

/*
 * 初始化电源管理
 * ESP32-S3运行在240MHz, 双核
 */
static void pm_init(void) {
    esp_pm_config_esp32s3_t pm_cfg = {
        .max_freq_mhz = 240,
        .min_freq_mhz = 40,
        .light_sleep_enable = true
    };
    esp_pm_configure(&pm_cfg);
}

/*
 * 板级初始化入口
 * 在Micropython启动时调用
 */
void board_init(void) {
    // 初始化电源管理
    pm_init();
    
    // 初始化背光
    lcd_backlight_init();
    
    // 初始化I2C触摸屏
    i2c_touch_init();
    
    // 初始化I2S音频
    i2s_audio_init();
    
    // 初始化SD卡
    sdcard_init();
    
    printf("JC3248W535CN board initialized\n");
    printf("LCD: 320x480 QSPI, Touch: I2C, Audio: I2S, SD: SDIO\n");
}

/*
 * 软重启
 */
void micro_pycb_hard_reset(void) {
    esp_restart();
}

/*
 * 进入深度睡眠
 */
void micro_pycb_enter_deep_sleep(uint64_t us) {
    esp_deep_sleep_start();
}

/*
 * 获取随机数
 */
uint32_t get_random_seed(void) {
    return (uint32_t)esp_random();
}

/*
 * All rights reserved.
 * 官方网站：https://www.hcnsec.cn/
 */