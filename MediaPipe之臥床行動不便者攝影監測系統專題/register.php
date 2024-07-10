<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "mydb";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("連接數據庫失敗: " . $conn->connect_error);
}
// 檢查 users 資料表是否存在，如果不存在則創建
$sql_check_table = "SHOW TABLES LIKE 'users'";
$result = $conn->query($sql_check_table);

if ($result->num_rows == 0) {
    // 創建 users 資料表
    $sql_create_table = "CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL
    )";
    
    if ($conn->query($sql_create_table) === TRUE) {
        echo "成功創建資料表";
    } else {
        echo "創建資料表失敗: " . $conn->error;
    }
}
    

// 從 POST 請求中取得用戶輸入的資訊
$username = $_POST['username'];
$password = $_POST['password'];
$email = $_POST['email'];

// 檢查是否已存在相同用戶名
$check_query = "SELECT * FROM users WHERE username = ?";
$check_stmt = $conn->prepare($check_query);
// 使用 bind_param() 方法綁定參數，"s" 表示參數是字串類型，將 $username 綁定到查詢中的參數
$check_stmt->bind_param("s", $username);
// 執行程式，查詢用戶是否存在
$check_stmt->execute();
// 使用 get_result() 方法獲取查詢結果集
$check_result = $check_stmt->get_result();


// 如果已經存在相同用戶名，則顯示錯誤訊息
if ($check_result->num_rows > 0) {
    echo "該用戶名已被使用，請選擇其他用戶名。";
} else {
     // 插入新用戶資訊到資料庫中
    $insert_query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)";
    $insert_stmt = $conn->prepare($insert_query);
    $insert_stmt->bind_param("sss", $username, $password, $email);

    if ($insert_stmt->execute()) {
        $_SESSION['username'] = $username; // 將註冊用戶名儲存
        header("Location: loght.html");// 轉跳到指定頁面
        exit();
    } else {
        echo "註冊失败";
    }

    $insert_stmt->close();
}

$check_stmt->close();
$conn->close();
?>
