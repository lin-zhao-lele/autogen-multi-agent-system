"""
Unit tests for the Web Interface.
"""
import pytest
from fastapi.testclient import TestClient
from web.main import app


class TestWebInterface:
    """Test cases for the Web Interface."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "AutoGen Multi-Agent Code Generation System"
        
    def test_health_check_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        
    def test_api_docs_endpoints(self, client):
        """Test that API documentation endpoints are available."""
        # Test Swagger UI
        response1 = client.get("/docs")
        assert response1.status_code == 200
        
        # Test ReDoc
        response2 = client.get("/redoc")
        assert response2.status_code == 200
        
    def test_generate_code_endpoint(self, client):
        """Test the code generation endpoint."""
        # Test with valid request
        request_data = {
            "requirements": "Create a function that calculates fibonacci numbers",
            "language": "python",
            "complexity": "medium"
        }
        
        response = client.post("/api/v1/generate-code", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert "message" in data
        assert data["message"] == "Code generation task started"
        
    def test_generate_code_endpoint_validation(self, client):
        """Test validation for the code generation endpoint."""
        # Test with missing required field
        invalid_request = {
            "language": "python",
            "complexity": "medium"
        }
        
        response = client.post("/api/v1/generate-code", json=invalid_request)
        # Should return 422 for validation error
        assert response.status_code == 422
        
    def test_code_status_endpoint_not_found(self, client):
        """Test the code status endpoint with non-existent task."""
        response = client.get("/api/v1/code-status/non-existent-task-id")
        assert response.status_code == 404
        
    def test_agents_endpoint(self, client):
        """Test the agents listing endpoint."""
        response = client.get("/api/v1/agents")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
    def test_config_endpoint(self, client):
        """Test the config endpoint."""
        response = client.get("/api/v1/config")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        
    def test_api_info_endpoint(self, client):
        """Test the API info endpoint."""
        response = client.get("/api/v1/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "description" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])