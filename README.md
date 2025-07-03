# `Zoom Meeting` : [`Deployed`](https://zoomeet.pythonanywhere.com/)

```bash
# export your keys from https://marketplace.zoom.us/user/build
export ZOOM_CLIENT_ID="your_actual_zoom_client_id"
export ZOOM_CLIENT_SECRET="your_actual_zoom_client_secret"

# it will generate zoom_token.json
python main.py

# pull zoom-flask-app image
docker pull ghcr.io/imvickykumar999/zoom-flask-app:latest

# run at port 5000
docker run -p 5000:5000 \
  -e ZOOM_CLIENT_ID=your_client_id \
  -e ZOOM_CLIENT_SECRET=your_client_secret \
  -v $(pwd)/zoom_token.json:/app/zoom_token.json \
  ghcr.io/imvickykumar999/zoom-flask-app:latest
```

![image](https://github.com/user-attachments/assets/cf3cb7e4-f591-4961-a42c-9de6da8a6a4e)
![image](https://github.com/user-attachments/assets/b55c7773-bbc3-4762-90b8-eb7f03925f5d)
![image](https://github.com/user-attachments/assets/acd1d7e0-36fa-4e9f-b6b7-933eadfc4b6d)
