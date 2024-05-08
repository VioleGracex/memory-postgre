function openMapPopup() {
    var mapPopup = document.getElementById("mapPopup");
    mapPopup.classList.toggle("hidden");
    // Additional JavaScript logic to handle opening and closing the map popup
}
 // Function to open emoji picker
document.getElementById('emojiButton').addEventListener('click', function() {
    var textarea = document.getElementById('contentTextArea');
    var emojiPicker = new EmojiPicker();
    emojiPicker.addEventListener('emoji-click', function(event) {
        textarea.value += event.detail.unicode;
    });
    emojiPicker.showPicker(document.getElementById('emojiButton'));
    
});


/* <!-- JavaScript to handle media uploading and memory saving --> */


// Function to handle media uploading
function uploadMedia() {
    document.getElementById('images').click();
}

// Function to create a delete button
function createDeleteButton(container) {
    var deleteBtn = document.createElement('button');
    deleteBtn.classList.add('delete-btn'); // Initially hidden
    deleteBtn.innerHTML = '&times;'; // Unicode multiplication symbol (×) for delete
    deleteBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default behavior (i.e., redirection)
        container.remove(); // Remove the media item container
    });
    return deleteBtn;
}

// Function to create a full-screen button
function createFullScreenButton(img) {
    var fullScreenBtn = document.createElement('button');
    fullScreenBtn.classList.add('full-screen-btn'); // Initially hidden
    fullScreenBtn.innerHTML = '&#x26F6;'; // Unicode arrow for full-screen
    fullScreenBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default behavior (i.e., redirection)
        img.requestFullscreen(); // Display image in full-screen
    });
    return fullScreenBtn;
}

// Function to display uploaded media (image or video)
function displayMedia(file) {
    var container = document.createElement('div');
    container.classList.add('media-item-container');

    // Check if the file is an image
    if (file.type.startsWith('image/')) {
        var imgContainer = document.createElement('div');
        imgContainer.classList.add('media-item-wrapper');

        var img = document.createElement('img');
        img.classList.add('media-item');
        img.file = file;
        img.src = URL.createObjectURL(file);

        // Append the image to its container
        imgContainer.appendChild(img);
        container.appendChild(imgContainer);

        // Create and append delete button
        var deleteBtn = createDeleteButton(imgContainer);
        imgContainer.appendChild(deleteBtn);

        // Create and append full-screen button
        var fullScreenBtn = createFullScreenButton(img);
        imgContainer.appendChild(fullScreenBtn);
    }
    // Check if the file is a video
    else if (file.type.startsWith('video/')) {
        var video = document.createElement('video');
        video.classList.add('media-item');
        video.file = file;
        video.src = URL.createObjectURL(file);
        video.controls = true; // Show video controls

        // Append the video to its container
        videoContainer.appendChild(video);
        container.appendChild(videoContainer);

        // Create and append delete button for videos
        var deleteBtn = createDeleteButton(videoContainer);
        videoContainer.appendChild(deleteBtn);
    }

    // Append the container to the media belt
    document.getElementById('mediabelt').insertBefore(container, document.getElementById('uploadBtnContainer'));
}



// Event listener for the upload media button
document.getElementById('uploadMediaBtn').addEventListener('click', function () {
    document.getElementById('mediaInput').click();
});

// Event listener for media input change
document.getElementById('mediaInput').addEventListener('change', function () {
    var files = this.files;
    // Iterate over selected files and display media (image or video)
    for (var i = 0; i < files.length; i++) {
        displayMedia(files[i]);
    }
});