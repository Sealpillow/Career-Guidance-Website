// script.js

function updateThresholdValue() {
    const slider = document.getElementById('threshold');
    const valueDisplay = document.getElementById('threshold-value');
    valueDisplay.textContent = slider.value;
}

document.getElementById('find-jobs').addEventListener('click', function() {
    const threshold = document.getElementById('threshold').value;
    const jobsList = document.getElementById('jobs');
    jobsList.innerHTML = ''; // Clear previous results

    // Simulated job listings based on threshold (replace with actual data)
    const jobs = [
        { title: 'Software Engineer', threshold: 0.3 },
        { title: 'Data Scientist', threshold: 0.5 },
        { title: 'Web Developer', threshold: 0.7 },
        { title: 'Product Manager', threshold: 0.9 },
    ];

    jobs.forEach(job => {
        if (job.threshold <= threshold) {
            const listItem = document.createElement('li');
            listItem.textContent = job.title;
            jobsList.appendChild(listItem);
        }
    });
});

document.getElementById('download-csv').addEventListener('click', function() {
    const jobs = [
        { title: 'Software Engineer', threshold: 0.3 },
        { title: 'Data Scientist', threshold: 0.5 },
        { title: 'Web Developer', threshold: 0.7 },
        { title: 'Product Manager', threshold: 0.9 },
    ];

    let csvContent = "data:text/csv;charset=utf-8,Title,Threshold\n";
    jobs.forEach(job => {
        csvContent += `${job.title},${job.threshold}\n`;
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'job_results.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});