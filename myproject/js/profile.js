function enableEdit(inputId) {
    var inputField = document.getElementById(inputId);
    if (inputField.disabled) {
        inputField.removeAttribute('disabled');
    } else {
        inputField.setAttribute('disabled', 'disabled');
    }
}

document.getElementById('optionsBtn').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent the click event from bubbling up to document level
    document.getElementById('optionsMenu').classList.toggle('hidden');
    event.preventDefault(); // Prevent the default behavior of the button element
});


document.getElementById('changeAvatarOption').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default link behavior
    document.getElementById('avatarInput').click(); // Trigger the file input
});

// Event listener for changing avatar picture
document.getElementById('avatarInput').addEventListener('change', function(event) {
    var file = this.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            // Set the image source to the data URL
            document.getElementById('profilePicture').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// Function to handle cancel changes button click
function handleCancelChanges() {
    // Redirect to userfeed
    window.location.href = "{% url 'user_specific_feed' user_id=custom_user.id %}";
}

// Event listener for cancel changes button
document.getElementById('cancelChangesBtn').addEventListener('click', handleCancelChanges);

function uploadAvatar()
{
    event.preventDefault(); // Prevent the default link behavior
    document.getElementById('avatarInput').click(); // Trigger the file input
}
function uploadCover()
{
    event.preventDefault(); // Prevent the default link behavior
    document.getElementById('coverInput').click(); // Trigger the file input
}