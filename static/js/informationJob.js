var sectionName = localStorage.getItem('sectionName') || 'informationJob';
var isReloadedSection = localStorage.getItem('isReloadedSection') || 'true';
document.addEventListener("DOMContentLoaded", function() {
    console.log("loading");
    console.log("sectionName:", sectionName);
    console.log("isReloadedSection:", isReloadedSection);
    var sectionName = localStorage.getItem('sectionName');
    var isReloadedSection = localStorage.getItem('isReloadedSection');

    if (sectionName === null || sectionName === "undefined") {
        sectionName = "informationJob";
    }

    if (isReloadedSection == 'true') {
        var sections = document.querySelectorAll("#informationJob, #Insurance");

        // Ẩn tất cả các phần tử
        sections.forEach(function(section) {
            section.style.display = "none";
        });

        // Hiển thị phần tử tương ứng với nút bấm được nhấn
        document.getElementById(sectionName).style.display = "block";
        console.log("sectionName 1:", sectionName);
        localStorage.setItem('isReloadedSection', 'false');

    } else {
        var sections = document.querySelectorAll("#informationJob, #Insurance");
        // Ẩn tất cả các phần tử
        sections.forEach(function(section) {
            section.style.display = "none";
        });

        document.getElementById(sectionName).style.display = "block";
        console.log("sectionName 2 :", sectionName);
    }


    var sectionButtons = document.querySelectorAll(".btn.btn-sm");

    // Lặp qua từng nút bấm
    sectionButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            // Lấy giá trị của thuộc tính dữ liệu data-table
            var sectionName = this.dataset.table;
            if (sectionName === undefined || sectionName === "undefined") {
                console.log(123454566)
                return; // Thoát khỏi hàm nếu giá trị không tồn tại hoặc là "undefined"
            }
            localStorage.setItem('sectionName', sectionName);

            var sections = document.querySelectorAll("#informationJob, #Insurance");

            // Ẩn tất cả các phần tử
            sections.forEach(function(section) {
                section.style.display = "none";
            });

            // Hiển thị phần tử tương ứng với nút bấm được nhấn
            document.getElementById(sectionName).style.display = "block";
            console.log("sectionName 4 :", sectionName);
            localStorage.setItem('isReloadedSection', 'false');
        });
    });
});

function resetLocalStorage() {
    // Xóa toàn bộ dữ liệu trong localStorage
                localStorage.clear();
}