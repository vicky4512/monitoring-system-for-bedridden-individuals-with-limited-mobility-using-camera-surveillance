<?php
// 開啟 PHP session
session_start();
// 設定 MySQL 伺服器連接資訊
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "mydb";
// 連接到 MySQL 資料庫
$conn = new mysqli($servername, $username, $password, $dbname);
// 檢查連接是否成功，若失敗則輸出錯誤訊息並終止程式
if ($conn->connect_error) {
    die("連接數據庫失敗: " . $conn->connect_error);
}
// 從 POST 請求中取得用戶名和密碼
$username = $_POST['username'];
$password = $_POST['password'];
// 使用預備語句來防範 SQL 注入攻擊，檢索與用戶名相符的資料
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
$stmt->bind_param("s", $username);
$stmt->execute();
// 獲取查詢結果
$result = $stmt->get_result();
// 如果資料庫中存在相符的用戶名
if ($result->num_rows == 1) {
    // 獲取資料庫中的資料
    $row = $result->fetch_assoc();
    $storedPassword = $row['password'];
// 檢查輸入的密碼是否與資料庫中存儲的密碼相符
    if ($password === $storedPassword) {
         // 登入成功，將用戶名存入 session 中
        $_SESSION['username'] = $username; // 儲存登陸帳戶
        header("Location: check.php");// 導向到 "check.php" 頁面
        exit();
        // 密碼不相符時輸出登入失敗訊息
    } else {
         // 用戶名不存在時輸出登入失敗訊息
        echo "登入失败";
    }
} else {
    echo "登入失败";
}
// 關閉 prepared statement 和資料庫連接
$stmt->close();
$conn->close();
?>
