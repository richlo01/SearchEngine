# Search Engine
Created a search engine on the ICS repository, ranks the results, and returns them in under 200ms. We improved query results by implementing cosine
similarity between tokens and documents using term frequency - inverse document frequency. Before the search engine runs, we developed a scraper to create an
index that was sorted alphebetically. Here we would do word preprocessing and document duplicate checks using SimHash. This way, the results are accurate
and efficient since they were done before hand.

<br />An example image is as follow
<p align="center">
</p>
