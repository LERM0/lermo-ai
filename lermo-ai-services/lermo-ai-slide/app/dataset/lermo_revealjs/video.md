# Lermo Video


## Lermo Video iframe, youtube, embed
```html
<section>
    <iframe data-autoplay width="700" height="540" src="https://slides.com/news/auto-animate/embed" frameborder="0"></iframe>
</section>

<section data-background-iframe="https://www.youtube.com/embed/h1_nyI3z8gI" data-background-interactive>
</section>
```

## Lermo Video, file
```html
<section>
    <video src="http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4" data-autoplay></video>
</section>
```

## Lermo Video, Background Video

```html
<section data-background-video="http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4">
</section>
```

```html
<section data-background-video="https://static.slid.es/site/homepage/v1/homepage-video-editor.mp4" data-background-video-loop data-background-video-muted>
</section>
```

## Lermo Video, Lazy Loading

```html
<section>
  <img data-src="image.png">
  <iframe data-src="https://hakim.se"></iframe>
  <video>
    <source data-src="video.webm" type="video/webm" />
    <source data-src="video.mp4" type="video/mp4" />
  </video>
</section>
```