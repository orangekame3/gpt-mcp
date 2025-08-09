# GPT MCP Server Example

## Available Models

The GPT MCP server supports the following OpenAI models with web search capabilities:

- **o3** - Latest OpenAI model with native web search
- **gpt-5** - Advanced model with web search support

## Weather Query Examples

**Query:** 大阪梅田の今日の天気はどうですか？気温、湿度、降水確率などの詳しい情報を教えてください。

### Model: gpt-5

**Weather Information for Osaka Umeda (August 9, 2025)**

**Current Weather:**
- Condition: くもりがち (Mostly cloudy)
- Temperature: 30°C (86°F)

**Today's Forecast:**
- **Morning to Evening:** くもり時々日差し (Cloudy with occasional sunshine)
- **Late Night:** 23時ごろににわか雨の可能性 (Possible showers around 11 PM)

**Hourly Temperature:**
- 11:00 - 30°C
- 13:00 - 32°C (Daily high)
- 18:00 - 29°C  
- 23:00 - 26°C

**Temperature Range:**
- **High:** ~32°C
- **Low:** ~26°C (late night)

**Additional Notes:**
- Humidity and precipitation probability data were not available in the current data source
- Hot and humid conditions expected during the day
- Recommended to stay hydrated and carry an umbrella for potential evening showers

### Model: o3

**Weather Information for Osaka Umeda (August 9, 2025)**

**Current Weather (11:00 JST):**

- Condition: 薄曇り (Partly cloudy)
- Temperature: 30°C (86°F)
- Feels like: 33°C
- Humidity: ~54%
- Wind: Northwest 6 km/h
- Pressure: 1010 hPa

**Temperature Range:**

- High: 32°C (89°F) at 1-3 PM
- Low: 25°C (77°F) in early morning

**Hourly Forecast:**

| Time | Temp | Humidity | Precipitation | Conditions |
|------|------|----------|---------------|------------|
| 12:00 | 30°C | 52% | 0% | Cloudy |
| 13:00 | 32°C | 51% | 1% | Partly sunny |
| 15:00 | 32°C | 47% | 0% | Sunny |
| 18:00 | 29°C | 47% | 1% | Partly cloudy |
| 21:00 | 27°C | 59% | 2% | Clear |
| 23:00 | 26°C | 65% | 6% | Possible light showers |

**Additional Information:**

- UV Index: Very high (10) around noon
- Hot and humid day with potential for brief evening showers
- Recommended to stay hydrated and use sun protection

## Comparison Summary

This example demonstrates the MCP server's ability to:

1. List available OpenAI models (o3, gpt-5)
2. Perform web-enabled searches for real-time information
3. Return detailed, localized weather information in Japanese
4. Show different response styles between models:
   - **gpt-5**: More narrative format with general temperature ranges
   - **o3**: Highly structured with detailed hourly forecasts and data tables