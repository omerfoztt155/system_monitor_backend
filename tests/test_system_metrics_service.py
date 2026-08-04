"""
Unit tests for SystemMetricsService.

These tests never touch a real database or MQTT broker: the repositories
are replaced with MagicMock fakes via constructor injection (see
SystemMetricsService.__init__). That's the whole point of having tested
the "why lazy pool / why DI" changes earlier — this file is fast and can
run in any environment (including CI) with no Postgres required.
"""

import json
import pytest
from datetime import datetime
from unittest.mock import MagicMock
from backend.exceptions import DatabaseError, DeviceNotFoundError, InvalidPayloadError
from backend.models.device import Device
from backend.services.system_metrics_service import SystemMetricsService

VALID_PAYLOAD = json.dumps({
    "device_code": "laptop-01",
    "cpu_usage": 42.5,
    "ram_usage": 63.1,
    "disk_usage": 71.9,
})

def make_service(device=None, find_device_side_effect=None):
    """Builds a SystemMetricsService backed by fake repositories."""
    device_repository = MagicMock()
    if find_device_side_effect is not None:
        device_repository.find_by_device_code.side_effect = find_device_side_effect
    else:
        device_repository.find_by_device_code.return_value = device

    metrics_repository = MagicMock()

    service = SystemMetricsService(
        device_repository=device_repository,
        system_metrics_repository=metrics_repository,
    )
    return service, device_repository, metrics_repository

def test_process_saves_valid_metric_for_known_device():
    device = Device(id=1, device_code="laptop-01", location="Home")
    service, device_repo, metrics_repo = make_service(device=device)

    service.process(VALID_PAYLOAD)

    device_repo.find_by_device_code.assert_called_once_with("laptop-01")
    metrics_repo.save.assert_called_once()

    saved_metric = metrics_repo.save.call_args.args[0]
    assert saved_metric.device_id == 1
    assert saved_metric.cpu_usage == 42.5
    assert saved_metric.ram_usage == 63.1
    assert saved_metric.disk_usage == 71.9
    assert isinstance(saved_metric.received_at, datetime)

def test_process_raises_device_not_found_and_does_not_save():
    service, _, metrics_repo = make_service(device=None)

    with pytest.raises(DeviceNotFoundError):
        service.process(VALID_PAYLOAD)

    metrics_repo.save.assert_not_called()

def test_process_raises_invalid_payload_for_malformed_json():
    service, _, metrics_repo = make_service(device=None)

    with pytest.raises(InvalidPayloadError):
        service.process("{not valid json")

    metrics_repo.save.assert_not_called()

@pytest.mark.parametrize(
    "missing_field", ["device_code", "cpu_usage", "ram_usage", "disk_usage"]
)

def test_process_raises_invalid_payload_for_missing_field(missing_field):
    data = {
        "device_code": "laptop-01",
        "cpu_usage": 1,
        "ram_usage": 1,
        "disk_usage": 1,
    }
    del data[missing_field]

    service, _, metrics_repo = make_service(device=None)

    with pytest.raises(InvalidPayloadError):
        service.process(json.dumps(data))

    metrics_repo.save.assert_not_called()

def test_process_raises_invalid_payload_for_non_numeric_field():
    data = {
        "device_code": "laptop-01",
        "cpu_usage": "high",  # should be a number, not a string
        "ram_usage": 1,
        "disk_usage": 1,
    }

    service, _, metrics_repo = make_service(device=None)

    with pytest.raises(InvalidPayloadError):
        service.process(json.dumps(data))

    metrics_repo.save.assert_not_called()

def test_process_does_not_swallow_database_errors_from_device_lookup():
    """The service intentionally does NOT catch DatabaseError raised by the
    repository — that decision belongs to the caller (MQTT handler / API),
    per the design from layer 1."""
    service, _, metrics_repo = make_service(
        find_device_side_effect=DatabaseError("connection lost")
    )

    with pytest.raises(DatabaseError):
        service.process(VALID_PAYLOAD)

    metrics_repo.save.assert_not_called()

def test_get_latest_delegates_to_repository():
    service, _, metrics_repo = make_service()
    metrics_repo.find_latest.return_value = "fake-metric"

    result = service.get_latest()

    assert result == "fake-metric"
    metrics_repo.find_latest.assert_called_once()

def test_get_all_delegates_to_repository():
    service, _, metrics_repo = make_service()
    metrics_repo.find_all.return_value = ["a", "b"]

    result = service.get_all()

    assert result == ["a", "b"]
    metrics_repo.find_all.assert_called_once()