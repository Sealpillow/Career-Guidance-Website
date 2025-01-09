function showPopUp(id) {
    document.getElementById(id).style.display = 'flex'; // Show the modal
}

function confirmUpload(id) {
    const popUpdiv = document.getElementById(id);
    const formId = popUpdiv.getAttribute('form_id');
    if(formId)
    {
        document.getElementById(formId).submit();
    }
    closeModal(id); // Close the modal
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none'; // Hide the modal
}