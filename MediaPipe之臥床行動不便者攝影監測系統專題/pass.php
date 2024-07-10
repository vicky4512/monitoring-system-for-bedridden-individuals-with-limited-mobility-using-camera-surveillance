<?php
use PHPMailer\PHPMailer\PHPMailer as PHPMailer;
use PHPMailer\PHPMailer\Exception as PHPMailerException;

require 'c:/xampp/htdocs/phpEmail/PHPMailer/src/PHPMailer.php';
require 'c:/xampp/htdocs/phpEmail/PHPMailer/src/Exception.php';
require 'c:/xampp/htdocs/phpEmail/PHPMailer/src/SMTP.php';

// Step 1: 資料庫設定
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "mydb";

// Step 2: 建立與資料庫的連接
$conn = new mysqli($servername, $username, $password, $dbname);

// 確認連線是否成功
if ($conn->connect_error) {
    die("資料庫連接失敗: " . $conn->connect_error);
}

// Step 3: 取得用戶輸入的email
if (isset($_POST['email'])) {
    $email = $_POST['email'];

    // Step 4: 查詢用戶密碼
    $sql = "SELECT password FROM users WHERE email = '$email'";
    $result = $conn->query($sql);

    if ($result->num_rows === 1) {
        $row = $result->fetch_assoc();
        $password = $row['password'];

        // Step 5: 發送email給用戶
        $to = $email;
        $subject = '您的密碼已發送';
        $message = '<html><body>';
        $message .= '<h1>您的密碼已發送</h1>';
        $message .= '<p>您的密碼是：' . $password . '</p>';
        $message .= '</body></html>';

        // 設定 SMTP 伺服器和帳戶資訊
        $mail = new PHPMailer(true);
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com';
        $mail->Port = 587;
        $mail->SMTPAuth = true;
        $mail->Username = 'vickylyj3@gmail.com';
        $mail->Password = 'xdmwmlqqpxksaayo';

        $mail->setFrom('from@example.com', 'Your password');
        $mail->addAddress($to, 'Recipient Name');

        $mail->isHTML(true);
        $mail->Subject = $subject;
        $mail->Body = $message;
        $mail->SMTPSecure = 'tls';

        // 設定郵件內容的編碼為UTF-8
        $mail->CharSet = 'UTF-8';

        // 忽略 SSL 憑證驗證
        $mail->SMTPOptions = array(
            'ssl' => array(
                'verify_peer' => false,
                'verify_peer_name' => false,
                'allow_self_signed' => true
            )
        );

        // 發送email
        if ($mail->send()) {
            echo "密碼已發送至您的電子郵件地址。請檢查您的郵件。";
        } else {
            echo "無法發送email，請稍後再試。";
        }
    }
}
?>
