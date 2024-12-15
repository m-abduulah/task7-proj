import pytest
import pickle

# Load the model
MODEL_PATH = r"model.pkl"
with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

@pytest.fixture
def sample_data():
    return [
        ([50, 10], 1),  # Example input and expected output (change as needed)
        ([30, 5], 0),
        ([70, 20], 1)
    ]

# Test if the model is loaded correctly
def test_model_loaded():
    assert model is not None, "Model should be loaded successfully."

# Test prediction shape
def test_prediction_shape():
    prediction = model.predict([[50, 10]])
    assert len(prediction) == 1, "Prediction should return a single output."

# Test model input validation
def test_model_input_validation():
    with pytest.raises(ValueError):
        model.predict([["invalid", 10]])  # Invalid data type

    with pytest.raises(ValueError):
        model.predict([[50]])  # Incorrect input shape
