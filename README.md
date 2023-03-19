<p align="center">
<img src="https://projects.mitchellbreden.nl/assets/images/satellite-with-text.svg" width="300"><br>
</p>

# Flight Hunter

This is a Flight Hunter made with a Raspberry pi 3B+. It can take photos or videos and store them on an AWS S3 cloud.
This project was created because a Raspberry pi 3b+ has been in the closet for years.

## Screenshots

<video width="400" controls>
  <source src="https://projects.mitchellbreden.nl/assets/video/preview.mp4" type="video/mp4">
  Your browser does not support HTML video.
</video>

<video width="320" height="240" controls>
  <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
</video>

## Run Locally

Clone the project

```bash
  git clone https://github.com/MitchBred/flights.mitchellbreden.nl
```

Go to the project directory

```bash
  cd flights.mitchellbreden.nl
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Tips:

- If you install this project on a Raspberry pi check first [Lessons Learned]

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`AWS_ACCESS_KEY_ID`

`AWS_SECRET_ACCESS_KEY`

`X_RAPID_API_KEY`

`X_RAPID_API_HOST`

`LAT`

`LON`

`KM_RADIUS`

`CAPTURE`

`OS`

## Features

- Live previews.
- Choose between image or video capturing.
- Calculate radius from your home.
- Send images trough Whatsapp.

## Tech Stack

**Client:** Python

**Server:** Laravel (PHP)

## Roadmap

- Standby mode on Raspberry pi when there are clouds.

- Monitoring Raspberry pi 3b+ (voltage, etc.).

- Add USB camera (better quality) with 360° view.

- Add solar panel to power bank.

- Send images or videos to your own whatsapp chat.
  https://github.com/Ankit404butfound/PyWhatKit

- Get automatically Latitude and Longitude from Raspberry pi.

[Related project](https://github.com/MitchBred/flights.mitchellbreden.nl-backend)

- Create archive page.

- Laravel app to an Node app

## Demo

https://projects.mitchellbreden.nl/flights

## Related

Here the server side of the related project

[SOON](https://github.com/MitchBred/flights.mitchellbreden.nl-backend)

## Lessons Learned

What did you learn while building this project? What challenges did you face and how did you overcome them?

- Install 64 bits version ubuntu server and not a 32 bits version.
- Can only use capture functions on the Raspberry pi.
- [Check](https://youtu.be/bwE4Mr-2ksQ) the right user privileges before you install the project on the Raspberry pi.
- [Check how to](youtube.com/watch?v=nx8gDSS1vO4) connect the camera connection through the Raspberry pi.

## Authors

- [@MitchBred](https://www.github.com/MithBred)

## License

[MIT](https://choosealicense.com/licenses/mit/)

