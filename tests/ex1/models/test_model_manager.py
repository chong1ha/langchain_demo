import pytest
from io import StringIO
from unittest.mock import AsyncMock, patch, MagicMock
from ex1.models.model_manager import ModelManager


@pytest.mark.asyncio
@patch('ex1.models.model_manager.OpenAI')
async def test_get_response_async(MockOpenAI):
    """
    비동기 처리 확인
    """
    # Arrange: OpenAI Mock 처리
    mock_instance = MockOpenAI.return_value
    mock_instance.ainvoke = AsyncMock(return_value="Mocked async response")

    model_manager = ModelManager()

    # Act: 비동기 메서드 호출
    prompt = "What is the capital of France?"
    response = await model_manager.get_response_async(prompt)

    # Assert: 응답 확인
    assert response == "Mocked async response"
    mock_instance.ainvoke.assert_awaited_once_with(prompt)
# End of test_get_response_async

@patch('ex1.models.model_manager.OpenAI')
def test_get_batch_response_sync(MockOpenAI):
    """
    배치 처리 확인
    """
    # Arrange: OpenAI Mock 처리
    mock_instance = MockOpenAI.return_value
    mock_instance.invoke.return_value = "Mocked response"

    model_manager = ModelManager()
    
    # Act: 
    prompts = [
        "What is the capital of France?",
        "What is the capital of Germany?"
    ]
    
    responses = model_manager.get_batch_response_sync(prompts)

    # Assert: 응답 일치 및 메소드 호출 횟수 확인
    assert responses == ["Mocked response", "Mocked response"]
    assert mock_instance.invoke.call_count == 2
# End of test_get_batch_response_sync

@pytest.mark.asyncio
@patch('ex1.models.model_manager.OpenAI')
async def test_get_batch_response_async(MockOpenAI):
    """
    비동기 배치 처리 확인
    """
    # Arrange: OpenAI Mock 처리
    mock_instance = MockOpenAI.return_value
    mock_instance.abatch = AsyncMock(return_value=["Mocked response", "Mocked response", "Mocked response"])

    model_manager = ModelManager()

    # Act: 비동기 배치 처리 호출
    prompts = [
        "What is the capital of France?",
        "What is the capital of Germany?",
        "What is the capital of Spain?"
    ]

    responses = await model_manager.get_batch_response_async(prompts)

    # Assert: 응답 일치 및 메소드 호출 횟수 확인
    assert responses == ["Mocked response", "Mocked response", "Mocked response"]
    assert mock_instance.abatch.call_count == 1
# End of test_get_batch_response_async

@patch('ex1.models.model_manager.OpenAI')
def test_stream_response_sync(MockOpenAI):
    """
    스트리밍 동기 응답 처리 확인
    """
    # Arrange: OpenAI Mock 처리
    mock_instance = MockOpenAI.return_value
    mock_instance.stream_sync.return_value = iter(["Chunk 1", "Chunk 2", "Chunk 3"])

    model_manager = ModelManager()

    # Act: 
    prompt = "What is the capital of France?"
    
    # StringIO를 사용하여 print 내용 캡처
    with patch("builtins.print") as mock_print:
        model_manager.stream_response_sync(prompt)

        # Assert: 각 청크 출력 확인
        mock_print.assert_any_call("Chunk 1", end="", flush=True)
        mock_print.assert_any_call("Chunk 2", end="", flush=True)
        mock_print.assert_any_call("Chunk 3", end="", flush=True)
    
    # Assert: 호출 횟수 확인
    mock_instance.stream_sync.assert_called_once_with(prompt)
# End of test_stream_response_sync