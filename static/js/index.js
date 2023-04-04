window.onload = function () {
    let page_elements = document.getElementsByClassName('page-link');
    Array.from(page_elements).forEach(function (element) {
        element.addEventListener('click', function () {
            document.getElementById('page').value = this.dataset.page;
            document.getElementById('filterForm').submit();
        });
    });

    document.getElementById('filterForm').addEventListener('reset', function() {
        document.querySelectorAll('a.btn.active').forEach(buttonElement => {
            const button = bootstrap.Button.getOrCreateInstance(buttonElement);
            button.toggle();
        });
    });

    document.getElementById('filterForm').addEventListener('submit', function() {
        alert('!');
    });
};