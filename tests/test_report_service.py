import pytest
from unittest.mock import Mock, MagicMock
from app.Repository.IRepository import IRepository
from app.services.report_service import ReportService


@pytest.fixture
def mock_repository():
    return Mock(spec=IRepository)


@pytest.fixture
def report_service(mock_repository):
    return ReportService(repository=mock_repository)


def test_get_target_names(report_service, mock_repository):
    mock_repository.get_all_fuzz_target_names.return_value = [
        'target1', 'target2']
    target_names = report_service.get_target_names()
    assert target_names == ['target1', 'target2']
    mock_repository.get_all_fuzz_target_names.assert_called_once()


def test_get_target_report_success(report_service, mock_repository):
    mock_target = Mock()
    mock_target.gen_target_report.return_value = 'report'
    mock_repository.get.return_value = mock_target

    target_report = report_service.get_target_report('target1')
    assert target_report == 'report'
    mock_repository.get.assert_called_once_with('target1')
    mock_target.gen_target_report.assert_called_once()


def test_get_target_report_none(report_service, mock_repository):
    mock_target = Mock()
    mock_target.gen_target_report.return_value = None
    mock_repository.get.return_value = mock_target

    target_report = report_service.get_target_report('target1')
    assert target_report == (None, None)
    mock_repository.get.assert_called_once_with('target1')
    mock_target.gen_target_report.assert_called_once()


def test_get_target_report_exception(report_service, mock_repository):
    mock_repository.get.side_effect = Exception('error')

    target_report = report_service.get_target_report('target1')
    assert target_report is None
    mock_repository.get.assert_called_once_with('target1')


def test_get_target_report_img_path(report_service, mock_repository):
    mock_repository.get_plot_imgs.return_value = ['img1.png', 'img2.png']
    img_paths = report_service.get_target_report_img_path('target1')
    assert img_paths == ['img1.png', 'img2.png']
    mock_repository.get_plot_imgs.assert_called_once_with('target1')
