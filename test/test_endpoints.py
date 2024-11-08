from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# arrange
# act
# assert

def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_generate_story():
    body_json = {
        "title": "Echoes of Destiny",
        "settings": {
            "size": "short",
            "attributes": [
                {
                    "name": "environment",
                    "value": "lush forests and towering mountains"
                },
                {
                    "name": "time period",
                    "value": "futuristic with ancient ruins"
                }
            ]
        },
        "characters": [
            {
                "name": "Alex",
                "attributes": [
                    {
                        "name": "age",
                        "value": "18"
                    },
                    {
                        "name": "ability",
                        "value": "telekinesis"
                    }
                ]
            },
            {
                "name": "Luna",
                "attributes": [
                    {
                        "name": "age",
                        "value": "20"
                    },
                    {
                        "name": "ability",
                        "value": "illusion"
                    }
                ]
            },
            {
                "name": "Draco",
                "attributes": [
                    {
                        "name": "age",
                        "value": "35"
                    },
                    {
                        "name": "ability",
                        "value": "fire"
                    }
                ]
            }
        ],
        "plots": 1,
        "endings": 1
    }

    # act
    response = client.post("/generate/story", json=body_json)
    # assert
    assert response.status_code == 200


def test_generate_dialog():
    # arrange
    body_json = {
        "story": "In a world where technology and magic coexist, a young man named Alex embarks on an adventure to uncover the secrets of his lineage. As he navigates through mystical forests and futuristic cities, he meets unexpected allies and faces formidable foes. With each step, he learns more about his family's ancient legacy and the powers that lie dormant within him. Along the way, he must choose between embracing his magical heritage or the technological advancements of his time, ultimately discovering that the true power lies in the balance between the two.",
        "settings": {
            "number_of_scenes": 1,
            "number_of_characters": 1
        },
        "characters": [
            {
                "name": "Alex",
                "attributes": [
                    {
                        "name": "age",
                        "value": "18"
                    },
                    {
                        "name": "magical ability",
                        "value": "telekinesis"
                    }
                ]
            },
            {
                "name": "Luna",
                "attributes": [
                    {
                        "name": "age",
                        "value": "20"
                    },
                    {
                        "name": "magical ability",
                        "value": "illusion"
                    }
                ]
            },
            {
                "name": "Draco",
                "attributes": [
                    {
                        "name": "age",
                        "value": "35"
                    },
                    {
                        "name": "magical ability",
                        "value": "fire"
                    }
                ]
            }
        ]
    }
    # act
    response = client.post("/generate/dialog", json=body_json)
    # assert
    assert response.status_code == 200
