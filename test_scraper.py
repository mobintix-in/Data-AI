from app import app
import traceback

with app.test_client() as client:
    print("Sending POST request to /search...")
    response = client.post('/search', data={
        'country': 'India',
        'city': 'Surat',
        'niche': 'Street Food'
    })
    print("Response Status Code:", response.status_code)
    print("Response Data:")
    print(response.get_data(as_text=True))
