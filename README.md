# APC SmartConnect Home Assistant Integration

A complete Home Assistant custom integration for APC SmartConnect UPS devices. This integration provides comprehensive monitoring and control of your APC UPS through the SmartConnect cloud service.

## Features

### 🔌 Platform Support
- **Sensors**: Comprehensive monitoring of UPS metrics
- **Switches**: Control main and switched outlets (stub implementation, ready for library support)

### 📊 Sensor Capabilities
The integration dynamically discovers and creates sensors for:

#### Battery Metrics
- Battery capacity (%)
- Battery runtime (minutes/seconds)
- Battery status

#### Electrical Metrics
- Input voltage
- Output voltage
- Power consumption
- Apparent power
- Load percentage
- Current
- Frequency
- Energy consumption

#### Status & Monitoring
- UPS operational status
- UPS mode
- Temperature
- Network connectivity status

#### Alarms & Events
- Active alarm indicator
- Alarm count
- Last alarm message
- Active event indicator
- Event count
- Last event message

All alarm and event sensors include detailed attributes with full history.

### 🎛️ Switch Capabilities
- Main outlet control
- Individual switched outlet control
- Real-time status updates

**Note**: Outlet control methods are currently stub implementations awaiting support in the underlying Python library. The switches are ready to function once `set_outlet_state()` is implemented in the `apc-smartconnect` library.

### 🏠 Home Assistant Features
- **Config Flow**: Easy setup through Home Assistant UI
- **Async Updates**: Efficient coordinator-based updates every 5 minutes
- **Device Classes**: Proper Home Assistant device classes for all sensors
- **Entity Categories**: Diagnostic sensors properly categorized
- **Unique IDs**: Stable entity identifiers
- **Icons**: Context-appropriate icons for all entities
- **Device Info**: Full device information including model, serial, firmware

## Installation

### Method 1: Manual Installation

1. Download this repository
2. Copy the `custom_components/apc_smartconnect` directory to your Home Assistant `custom_components` directory
   ```
   <config_dir>/custom_components/apc_smartconnect/
   ```
3. Restart Home Assistant
4. Add the integration through the Home Assistant UI

### Method 2: HACS (Home Assistant Community Store)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/Dwokfur/ha-apc-smartconnect`
6. Select category "Integration"
7. Click "Add"
8. Find "APC SmartConnect" in the integration list and install it
9. Restart Home Assistant
10. Add the integration through the Home Assistant UI

## Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **APC SmartConnect**
4. Enter your APC SmartConnect credentials:
   - **Email**: Your APC SmartConnect account email
   - **Password**: Your APC SmartConnect account password
5. Click **Submit**

The integration will automatically discover all your APC SmartConnect devices and create entities for available metrics, alarms, and outlets.

### Multiple Devices

The integration automatically handles multiple UPS devices. Each device will be created as a separate device in Home Assistant with its own set of entities.

## Usage

### Sensors

All sensors are automatically created and will update every 5 minutes. You can use them in:
- Automations
- Scripts
- Cards and dashboards
- Conditional logic

Example automation to notify on low battery:
```yaml
automation:
  - alias: "UPS Low Battery Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.apc_smart_ups_1500_battery_capacity
        below: 20
    action:
      - service: notify.notify
        data:
          message: "UPS battery is low: {{ states('sensor.apc_smart_ups_1500_battery_capacity') }}%"
```

### Switches

Control your UPS outlets using the switch entities:

```yaml
# Turn off outlet 1
service: switch.turn_off
target:
  entity_id: switch.apc_smart_ups_1500_outlet_1

# Turn on main outlet
service: switch.turn_on
target:
  entity_id: switch.apc_smart_ups_1500_main_outlet
```

**Note**: Outlet control is currently a stub implementation. Once the `apc-smartconnect` Python library supports outlet control via the `set_outlet_state()` method, these switches will function fully. The integration is ready to use this functionality as soon as the library is updated.

### Alarm & Event Monitoring

Monitor UPS alarms and events through dedicated sensors:
- `sensor.apc_smart_ups_1500_alarm_active` - Boolean indicating active alarms
- `sensor.apc_smart_ups_1500_alarm_count` - Number of active alarms
- `sensor.apc_smart_ups_1500_last_alarm` - Last alarm message
- Similar sensors for events

All alarm/event sensors include detailed attributes with the full list of alarms/events.

## Entity Naming

Entities follow this naming convention:
```
{device_name}_{metric_type}
```

Examples:
- `sensor.apc_smart_ups_1500_battery_capacity`
- `sensor.apc_smart_ups_1500_input_voltage`
- `switch.apc_smart_ups_1500_outlet_1`

## Requirements

- Home Assistant 2023.1 or newer
- APC SmartConnect account
- Compatible APC UPS with SmartConnect capability
- Internet connection for cloud API access

### Python Dependencies

The integration requires the `apc-smartconnect` Python library (version 0.1.0 or newer), which will be automatically installed by Home Assistant.

## Troubleshooting

### Cannot connect to APC SmartConnect
- Verify your credentials are correct
- Ensure your APC SmartConnect account is active
- Check your internet connection
- Verify the APC SmartConnect service is operational

### Entities not updating
- Check Home Assistant logs for errors
- Verify network connectivity
- Ensure the integration is configured correctly
- Try reloading the integration

### Outlet controls not working
- This is expected - outlet control is a stub implementation
- The functionality will work once the `apc-smartconnect` library implements the `set_outlet_state()` method
- Monitor the library repository for updates

### Missing sensors
- Not all UPS models support all metrics
- Sensors are only created for metrics provided by your specific device
- Check the device capabilities in the APC SmartConnect app

## Development & Contributing

### Project Structure
```
custom_components/apc_smartconnect/
├── __init__.py          # Integration setup and coordinator
├── config_flow.py       # UI configuration flow
├── const.py            # Constants and sensor definitions
├── manifest.json       # Integration metadata
├── sensor.py           # Sensor platform implementation
└── switch.py           # Switch platform implementation
```

### Mock Client

The integration includes a mock APC SmartConnect client for development and testing. In production, this should be replaced with the actual `apc-smartconnect` library implementation.

To integrate with the real library:
1. Update `__init__.py` to import the actual `APCSmartConnect` class
2. Replace the `MockAPCClient` with real client instantiation
3. Implement the `set_outlet_state()` method in the library

### Adding New Sensor Types

To add new sensor types:
1. Add the sensor definition to `SENSOR_TYPES` in `const.py`
2. Ensure the mock client returns the appropriate data
3. The sensor platform will automatically create entities for new metrics

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/Dwokfur/ha-apc-smartconnect/issues)
- **Discussions**: Join the conversation on [GitHub Discussions](https://github.com/Dwokfur/ha-apc-smartconnect/discussions)

## Disclaimer

This is a community-developed integration and is not officially affiliated with or endorsed by APC or Schneider Electric. Use at your own risk.

## Acknowledgments

- Home Assistant community for the excellent platform
- APC/Schneider Electric for the SmartConnect service

## Changelog

### Version 1.0.0
- Initial release
- Sensor platform with comprehensive UPS monitoring
- Switch platform for outlet control (stub implementation)
- Alarm and event sensors
- Config flow for UI-based setup
- Coordinator-based async updates
- Full Home Assistant integration features
