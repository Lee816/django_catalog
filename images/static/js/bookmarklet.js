const siteUrl = '//mysite.com:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWith = 250;
const minHeight = 250;

var head = document.getElementsByTagName('head')[0];
var link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random() * 9999999999999999);
head.appendChild(link);

var body = document.getElementsByTagName('body')[0];
boxHtml = `
<div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Select an image to bookmark:</h1>
    <div class="images"></div>
</div>
`;
console.log('boxHtml:', boxHtml);
body.innerHTML += boxHtml;

function bookmarkletLaunch() {
    bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');
    bookmarklet.style.display = 'block';
    bookmarklet.querySelector('#close')
        .addEventListener('click', function () {
            bookmarklet.style.display = 'none';
        });
}

bookmarkletLaunch();