# Brightcove-Dynamic-Ingest-App
This is a simple Python script that uses Brightcove's Dynamic Ingest API to upload video content parsed from MRSS and JSON feeds. 

The BC_01.py is our "Brightcove module" that contains oAuth, Dynamic Ingest, and deupe functions. Regarding the latter, this script relies upon the Brightcove CMS to act as a proxy database wherein we can check to see which videos have already been passed/uploaded to your Brightcove account. The feed parser portion of the script is very simple, using the Feedparser module. You can adjust the feed parser section of the code to suit your needs as long as all the required elements (video URL, name, description, tags) are passed to the response_array. 

As a reminder, you will need to create oAuth credentials using the commands in the Brightcove oAuth cURL Command file. Additionally, you will also need an API URL Read token from our Brightcove account so that the script can make a GET request to the Brightcove CMS to search for a specific video by video title. 

Dynamic Ingest API: 

Brightcove's Dynamic Ingest (DI) API is based on functionality where video source files are downloaded from the customer's storage location and specified renditions of the source files are created. The platform is cloud-centric, globally-distributed and based on modern practices to deliver best in class consistency and speed.

Strengths of the DI API are:

Predictability: Queue time and end-to-end processing time is determinate.
Speed: Brightcove's transcoding solution provides superior speed and scalability.
Features: Input format support, 99.9% transcoding success rate and a simplified usage workflow are just a few of the API's advantages.
Insight: Views and notifications into the progress of the transcoding status are provided.

