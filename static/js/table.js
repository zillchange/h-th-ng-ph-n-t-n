var startEntry = 1; // Define startEntry variable
var totalEntries = 0; // Define totalEntries variable
var endEntry = 0; // Define endEntry variable
var currentPage = 1; // Define current page
var totalPages = 1; // Define total pages
var columnNumber = 0;
var tableName = localStorage.getItem('tableName') || "userTable";
var tailUpdate = localStorage.getItem('tailUpdate') || "user";
var isReloaded = localStorage.getItem('isReloaded') || 'true';

console.log("table name 0:"+ tableName);
document.addEventListener("DOMContentLoaded", function() {
    console.log("loading")
    console.log("is reload"+isReloaded);
    console.log("table name:"+ tableName);
    if (isReloaded == 'true') {
        var sections = document.querySelectorAll("#userTable, #blockedUserTable, #accountTable");

        // Ẩn tất cả các phần tử
        sections.forEach(function(section) {
            section.style.display = "none";
        });
        // Hiển thị phần tử tương ứng với nút bấm được nhấn
        tableName = "userTable"; // Nếu không, thiết lập tableName thành "userTable"
        tailUpdate = "user"
        document.getElementById(tableName).style.display = "block";
        console.log("table name 1:"+ tableName);
        localStorage.setItem('isReloaded', 'false'); 

    }
    else{
        console.log("table name 2:"+ tableName);
        var sections = document.querySelectorAll("#userTable, #blockedUserTable, #accountTable");
        // Ẩn tất cả các phần tử
        sections.forEach(function(section) {
            section.style.display = "none";
        });
        document.getElementById(tableName).style.display = "block";
    }

    
    var tableButtons = document.querySelectorAll(".btn-sm");

    // Lặp qua từng nút bấm
    tableButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            // Lấy giá trị của thuộc tính dữ liệu data-table
            tableName = this.dataset.table + "Table";
            tailUpdate = this.dataset.table;
            console.log("table name when choose: " + tableName)
            console.log("tail when choose: " + tailUpdate)
            localStorage.setItem('tableName', tableName);
            localStorage.setItem('tailUpdate', tailUpdate);
            // Lấy tất cả các phần tử có id là userTable, blockedUserTable, accountTable
            var sections = document.querySelectorAll("#userTable, #blockedUserTable, #accountTable");

            // Ẩn tất cả các phần tử
            sections.forEach(function(section) {
                section.style.display = "none";
            });

            // Hiển thị phần tử tương ứng với nút bấm được nhấn
            document.getElementById(tableName).style.display = "block";
            // localStorage.setItem('isReloaded', 'true'); 
            
            startEntry = 1;
            totalEntries = 0;
            endEntry = 0;
            currentPage = 1;
            totalPages = 1;
            updateFooter();
            updateTable();
            checkBox();
        });
    });
    checkBox();
    console.log("table name 3:"+ tableName);
    // Gọi hàm updateTable() ngay sau khi tài liệu đã được tải hoàn toàn
    console.log("updateTable executed")
    updateTable();
});

function updateValue(){
    console.log("executing update value")
    localStorage.setItem('tableName', tableName);
    localStorage.setItem('tailUpdate', tailUpdate);
    localStorage.setItem('isReloaded', 'false'); 
    
}
function checkBox() {
    
        var checkBox = "selectAll"+ tailUpdate;
        console.log("checkBox", checkBox)
        
        document.getElementById(checkBox).addEventListener("click", function() {
            // Get all checkboxes in the table body
            var checkboxes = document.querySelectorAll("tbody input[type='checkbox']");
    
            // Loop through each checkbox and set its checked state to match the "Select All" checkbox
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = document.getElementById(checkBox).checked;
            });
        });
    
   
}


// search bar function
function changeEntries()
{
    currentPage = 1;
    if( columnNumber == -1)
        updateTableAll();
    else if(columnNumber == '')
        updateTable();
    else
       
        updateTableColumnSearch();
}
function search(column)
{
    currentPage = 1;
    if (column === 'all')
    {
        columnNumber = -1;
        updateTableAll();
    }

    else{
        columnNumber = column;
        updateTable();
    }

}
function columnSearch()
{
    columnNumber = '';
    currentPage = 1;
    updateTableColumnSearch();

}
function updateTable() {
        var rows, i, inputSearch;
        var table, td, txtValue;
        var filteredRows = [];

      
        console.log('update table');
        // Get the number of entries to display
        var selectEntry = "entries" + tailUpdate;
        var select = document.getElementById(selectEntry);
        var value = parseInt(select.value);
        var inputSearchTable = "myInput" + tailUpdate;
        inputSearch = document.getElementById(inputSearchTable).value.trim().toUpperCase();
        table = document.getElementById(tableName);


        rows = table.getElementsByTagName("tr");  


        // Get the table and table rows
        if ( inputSearch === "" ) {
            totalEntries = rows.length - 1;
            totalPages = parseInt((totalEntries-1) / value) + 1;
            
        } else {
            var emptyRow = document.createElement('tr');
            filteredRows.splice(0, 0, emptyRow);
            for (i = 1; i < rows.length; i++) {
                td = rows[i].getElementsByTagName("td")[columnNumber]; // Assuming the first column contains names
                if (td) {
                    txtValue = (td.textContent || td.innerText).trim();

                    if (txtValue.toUpperCase().indexOf(inputSearch) > -1) {

                        filteredRows.push(rows[i]);
                    }
                    else
                        rows[i].style.display = "none";
                }
            }
            rows = filteredRows;
            totalEntries = rows.length -1;
            num = parseInt((totalEntries - 1) / value);
            totalPages = num +1;

            
        }

    if(totalEntries == 0 )
    {
        startEntry = 0;
        endEntry = 0;
        currentPage = 0;
    }
    else if(totalPages == 1){
        startEntry = 1;
        endEntry = totalEntries;


    }
    else if(currentPage == 1)
    {
        startEntry = 1;
        endEntry = value;



    }

    else {
      startEntry = (currentPage - 1) * value + 1;
      endEntry = currentPage*value; 
    //   var visibleRows = document.querySelectorAll('#myTable tbody tr:not([style*="display: none"])');
    //   endEntry =  visibleRows.length + (currentPage-1)*value;

        if(endEntry > totalEntries)
        {
            endEntry = totalEntries

        }

        if(currentPage > totalPages)
        {
            currentPage = totalPages;
        }
        if(endEntry == startEntry & currentPage< totalPages)
        {
            endEntry = startEntry + value -1;

        }
        if(startEntry > endEntry)
        {
            startEntry = (currentPage - 1) * value + 1;
            var visibleRows = document.querySelectorAll('#myTable tbody tr:not([style*="display: none"])');
            endEntry =  visibleRows.length + (currentPage-1)*value;
        }

    }


    
    for (i = 1; i <= totalEntries; i++) { // Start from index 1 to skip the header row
        rows[i].style.display = "none";

   
    }

    for (i = startEntry; i <= endEntry; i++) {
            rows[i].style.display = "";

        }
    console.log("value:")
    console.log(totalEntries);
    console.log(startEntry);
    console.log(endEntry);
    console.log(currentPage);
    console.log(totalPages);
    updateFooter();
    generatePagination();

}

function updateTableAll() {
    var rows, i, inputSearch;
    var table, td, txtValue;
    var filteredRows = [];
    console.log('update table all');
    // Get the number of entries to display
    var selectEntry = "entries" + tailUpdate;
    var select = document.getElementById(selectEntry);
    var value = parseInt(select.value);
    var inputSearchTable = "myInput" + tailUpdate;
    inputSearch = document.getElementById(inputSearchTable).value.trim().toUpperCase();
    table = document.getElementById(tableName);
    rows = table.getElementsByTagName("tr");  

   
    // Get the table and table rows
    if ( inputSearch === "" ) {
        totalEntries = rows.length - 1;
        totalPages = parseInt((totalEntries-1) / value) + 1;
        
    } else {
        var emptyRow = document.createElement('tr');
        filteredRows.splice(0, 0, emptyRow);
        for (i = 1; i < rows.length; i++) {
            var flag = 0;
            td = rows[i].getElementsByTagName("td"); // Assuming the first column contains names
            for (var j = 1; j < td.length; j++) {
                if (td[j]) {
                    txtValue = (td[j].textContent || td[j].innerText).trim();
        
                    if (txtValue.toUpperCase().indexOf(inputSearch) > -1) {
                        flag = 1;
                        break;
                    }
                }
            }
            if (flag == 1) {
                filteredRows.push(rows[i]);
            } else {
                rows[i].style.display = "none";
            }
        }
        

        rows = filteredRows;
        totalEntries = rows.length -1;
        num = parseInt((totalEntries - 1) / value);
        totalPages = num +1;
    }

if(totalEntries == 0 )
{
    startEntry = 0;
    endEntry = 0;
    currentPage = 0;
}
else if(totalPages == 1){
    startEntry = 1;
    endEntry = totalEntries;


}
else if(currentPage == 1)
{
    startEntry = 1;
    endEntry = value;



}

else {
  startEntry = (currentPage - 1) * value + 1;
  endEntry = currentPage*value; 

    if(endEntry > totalEntries)
    {
        endEntry = totalEntries

    }

    if(currentPage > totalPages)
    {
        currentPage = totalPages;
    }
    if(endEntry == startEntry & currentPage< totalPages)
    {
        endEntry = startEntry + value -1;

    }
    if(startEntry > endEntry)
    {
        startEntry = (currentPage - 1) * value + 1;
        var visibleRows = document.querySelectorAll('#myTable tbody tr:not([style*="display: none"])');
        endEntry =  visibleRows.length + (currentPage-1)*value;
    }

}

for (i = 1; i <= totalEntries; i++) { // Start from index 1 to skip the header row
    rows[i].style.display = "none";


}

for (i = startEntry; i <= endEntry; i++) {
        rows[i].style.display = "";

    }
updateFooter();
generatePagination();



}

function updateTableColumnSearch() {
    var rows, i;
    var table, td, txtValue;
    var filteredRows = [];
    var inputColumnSearchArray =[];
    console.log("update table column search");
    // Get the number of entries to display
    var selectEntry = "entries" + tailUpdate;
    var select = document.getElementById(selectEntry);
    var value = parseInt(select.value);
    var inputSearchTable = "myInput" + tailUpdate;
    inputSearch = document.getElementById(inputSearchTable).value.trim().toUpperCase();
    table = document.getElementById(tableName);

    rows = table.getElementsByTagName("tr"); 
    var searchTable = "#columnSearch"+ tailUpdate;
    var columnSearchInputs = document.querySelectorAll(searchTable);
    columnSearchInputs.forEach(function(input) {
        var value = input.value.trim().toUpperCase();
        var columnIndex = input.getAttribute('data-index');
        if( value != "")
            inputColumnSearchArray.push([value, columnIndex]);
    });
    // Get the table and table rows
        var emptyRow = document.createElement('tr');
        filteredRows.splice(0, 0, emptyRow);
        for( i = 1; i < rows.length; i++)
        {
            var count = 0;
            for (var j = 0; j < inputColumnSearchArray.length; j++) {
                td = rows[i].getElementsByTagName("td")[inputColumnSearchArray[j][1]]; // Assuming the first column contains names
                    if (td) {
                        txtValue = (td.textContent || td.innerText).trim();         
                        if (txtValue.toUpperCase().indexOf(inputColumnSearchArray[j][0]) > -1) {
                            count++;
                        }
                    }
            }
            if (count == inputColumnSearchArray.length) {
                filteredRows.push(rows[i]);
            } else {
                rows[i].style.display = "none";
            }

        }
        rows = filteredRows;
        totalEntries = rows.length -1;
        num = parseInt((totalEntries - 1) / value);
        totalPages = num +1;
    

if(totalEntries == 0 )
{
    startEntry = 0;
    endEntry = 0;
    currentPage = 0;
}
else if(totalPages == 1){
    startEntry = 1;
    endEntry = totalEntries;


}
else if(currentPage == 1)
{
    startEntry = 1;
    endEntry = value;



}

else {
  startEntry = (currentPage - 1) * value + 1;
  endEntry = currentPage*value; 

    if(endEntry > totalEntries)
    {
        endEntry = totalEntries

    }

    if(currentPage > totalPages)
    {
        currentPage = totalPages;
    }
    if(endEntry == startEntry & currentPage< totalPages)
    {
        endEntry = startEntry + value -1;

    }
    if(startEntry > endEntry)
    {
        startEntry = (currentPage - 1) * value + 1;
        var visibleRows = document.querySelectorAll('#myTable tbody tr:not([style*="display: none"])');
        endEntry =  visibleRows.length + (currentPage-1)*value;
    }

}

for (i = 1; i <= totalEntries; i++) { // Start from index 1 to skip the header row
    rows[i].style.display = "none";


}

for (i = startEntry; i <= endEntry; i++) {
        rows[i].style.display = "";

    }
updateFooter();
generatePagination();
console.log(totalEntries);
console.log(startEntry);
console.log(endEntry);
console.log(currentPage);
console.log(totalPages);


}
function prevPage() {
    if (currentPage > 1) {
        currentPage = currentPage - 1;
        if( columnNumber == -1)
            updateTableAll();
        else if(columnNumber == '')
            updateTable();
        else
            updateTableColumnSearch();
    }
}


function nextPage() {
    if (currentPage < totalPages) {
        currentPage = currentPage + 1;
        if( columnNumber == -1)
            updateTableAll();
        else if(columnNumber == '')
            updateTable();
        else     
            updateTableColumnSearch();
    }
}


function updateFooter() {
        console.log("update footer");
        s = "startEntry" + tailUpdate;
        e = "endEntry" + tailUpdate;
        te = "totalEntries" + tailUpdate;
        c = "currentPage" + tailUpdate;
        tp = "totalPages" + tailUpdate;
        var startSpan = document.getElementById(s);
        var endSpan = document.getElementById(e);
        var totalSpan = document.getElementById(te);
        var currentPageSpan = document.getElementById(c);
        var totalPagesSpan = document.getElementById(tp);

        startSpan.textContent = startEntry;
        endSpan.textContent = endEntry;
        totalSpan.textContent = totalEntries; 
        currentPageSpan.textContent = currentPage;
        totalPagesSpan.textContent = totalPages;


}

function generatePagination() {
    console.log("Generating pagination")
    var container = 'paginationContainer'+ tailUpdate;
    var paginationContainer = document.getElementById(container);
    paginationContainer.innerHTML = '';

    var maxRectangles = 6; // Maximum number of rectangles
    var startPage, endPage;

    // Adjust the start page to ensure symmetry
    if (totalPages <= maxRectangles) {
        startPage = 1;
        endPage = totalPages;
    } else {
        startPage = Math.max(1, currentPage - Math.floor(maxRectangles / 2));
        endPage = Math.min(startPage + maxRectangles - 1, totalPages);
        // Adjust the start page again if necessary to ensure that there are exactly maxRectangles displayed
        startPage = Math.max(1, endPage - maxRectangles + 1);
    }

    for (var i = startPage; i <= endPage; i++) {
        var div = document.createElement('div');
        div.textContent = i;
        div.className = 'pagination-item';
        if (i === currentPage) {
            div.classList.add('active');
        }
        div.onclick = function() {
            changePage(parseInt(this.textContent));
        };
        paginationContainer.appendChild(div);
    }
}


function changePage(page)
{
    currentPage = page;
    if( columnNumber == -1)
        updateTableAll();
    else if(columnNumber == '')
        updateTable();
    else 
        updateTableColumnSearch();
}

