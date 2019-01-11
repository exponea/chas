/* Restart a job button */
$("form").submit(function(e) {
    e.preventDefault();
    const job_name = $(this).serializeArray()[0].value;
    $.ajax({
        url: `/jobs/${job_name}/run`,
        data: null,
        type: "POST",
        success: function(response) {
            console.log(response);
            setTimeout(() => {
                location.reload();
            }, 500);
        },
        error: function(error) {
            console.log(error);
        }
    });
});