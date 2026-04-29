document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("student-search");
    const rows = document.querySelectorAll("#student-table-body tr");
    const noResultsMessage = document.getElementById("no-results-message");
    const tableContainer = document.getElementById("table-container");

    if (!searchInput || !rows.length || !tableContainer) {
        return;
    }

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.toLowerCase().trim();
        let visibleCount = 0;

        rows.forEach(function (row) {
            const searchableText = row.dataset.search;
            const matches = searchableText.includes(query);

            row.style.display = matches ? "" : "none";

            if (matches) {
                visibleCount++;
            }
        });

        const hasResults = visibleCount > 0;

        tableContainer.classList.toggle("d-none", !hasResults);

        if (noResultsMessage) {
            noResultsMessage.classList.toggle("d-none", hasResults);
        }
    });
});