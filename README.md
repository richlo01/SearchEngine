# Search Engine
Created a search engine on the ICS repository, ranks the results, and returns them in under 200ms. We improved query results by implementing cosine
similarity between tokens and documents using term frequency - inverse document frequency. Before the search engine runs, we developed a scraper to create an
index that was sorted alphebetically. Here we would do word preprocessing and document duplicate checks using SimHash. This way, the results are accurate
and efficient since they were done before hand.

<br />An example image is as follows:
<p align="center">
  <img src="https://user-images.githubusercontent.com/47437080/121440415-b5c8f980-c93c-11eb-9caf-3ee20daabe13.png" width="1000">
</p>
