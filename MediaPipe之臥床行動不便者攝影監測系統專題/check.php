<!DOCTYPE html>
<html>
<head>
  <title>使用者列表</title>
  <meta charset="UTF-8">
  <style>
    body {
        background-color: Moccasin; 
    }
    form {
       text-align: center; /* 將內容置中 */
        margin-top: 20px; /* 調整上邊距增加間距 */     
        padding: 20px; /* 調整內邊距以增加空間 */
    }
    table {
      border-collapse: collapse;
      width: 100%;
      background-color: white;

    }

    th, td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }

    /* 響應式設計 */
    @media screen and (max-width: 600px) {
      table {
        font-size: 12px;
      }

      th, td {
        padding: 4px;
      }
    }

    /* 新增的CSS代碼 */
    button {
      border: none;
      background-color: transparent;
      padding: 0;
      cursor: pointer;
    }

    /* 按鈕樣式 */
    button {
      border: none;
      background-color: transparent;
      padding: 0;
      cursor: pointer;
    }
 
    /* 查詢按鈕 */
    input[type="submit"] {
      font-size: 20px;
      padding: 5px 10px;
      background-color: green;
      color: white;
      text-decoration: none; /* 去除超連結的底線 */
      border: none; /* 移除邊框 */
    }

    /*登出按鈕 */
    a button[type="button"] {
       font-size: 20px;
       padding: 5px 10px;
       background-color: green;
       color: white;
       text-decoration: none; /* 去除超連結的底線 */
    }

    /* 添加綠色背景顏色 */
    button[type="submit"] {
      background-color: green;
      color: white; /* 調整文字顏色為白色，以便與綠色背景對比 */
    }
    h1 {
       padding: 20px; /* 調整h1元素的內邊距 */
       text-align: center; /* 將文字置中 */
       background-color: Orange; /* 設置橘色背景 */
       color: white; /* 設置字體顏色為白色 */
    }
     
    
    
  </style>
  <script>
        window.onload = function() {
         // 檢查是否有"Fallen Icon"，並執行相應的動作
          var stageImages = document.querySelectorAll("td:nth-child(2) img");
          var hasFallen = false;
          for (var i = 0; i < stageImages.length; i++) {
              if (stageImages[i].alt === "Fallen Icon") {
                hasFallen = true;
                break;
              }
          }

          if (hasFallen) {           
            showAlert("對象處摔落狀態");
            playAlarm();
            
          } else {
            showAlert("對象處於安全狀態");
          }
        }
        // 顯示警告訊息
        function showAlert(message) {
            alert(message);
        }
        function playAlarm() {
            // 使用 Audio 元素播放警報聲
            var audio = document.getElementById("alarmAudio");
            audio.play();
        }
</script>

<!-- PHP腳本 -->
<?php
session_start();

// 檢查是否有登入帳號訊息
if (!isset($_SESSION['username'])) {
    header("Location: loght.php");
    exit();
}

$login_user = $_SESSION['username'];

// 連接資料庫
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "mydb";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("連接數據庫失敗: " . $conn->connect_error);
}

// 顯示登錄帳號+用戶列表標題
echo "<h1>" . $login_user . " 查詢使用者狀態</h1>";

?>


<!DOCTYPE html>
<html>
<head>
   
    <title>使用者列表</title>
   
</head>
<body>
  <audio id="alarmAudio" src="fall.mp3"></audio>
    <!-- 添加表單輸入日期 -->
    <form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
    <label for="search_date">選擇日期：</label>
    <input type="date" id="search_date" name="search_date" required>
        <br><br>
        <input type="submit" value="查詢">
        <a href="loght.html"><button type="button">登出</button></a> <!-- 使用一個名為 "logoht.php" 的登出頁面 -->
    </form>

    <br>

    <table>
        <tr>
            <th>Datetime</th>
            <th>Stage</th>
            <!-- 其他列 -->
        </tr>
        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $search_date = $_POST["search_date"];
            $sql = "SELECT * FROM pose_data WHERE DATE(datetime) = '$search_date' ORDER BY datetime DESC";
            $result = $conn->query($sql);

            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    echo "<tr>";
                    echo "<td>" . $row["datetime"] . "</td>";
                    echo "<td>";
                    if ($row["stage"] == "safe :)") {
                        echo "<img src='staf-removebg-preview (1).png' alt='Safe Icon'>";
                    } elseif ($row["stage"] == "stand up !!") {
                        echo "<img src='stand-removebg-preview (1).png' alt='Stand Up Icon'>";
                    } elseif ($row["stage"] == "fallen :(") {
                        echo "<img src='fall-removebg-preview .png' alt='Fallen Icon'>";
                    } else {
                        echo $row["stage"];
                    }
                    echo "</td>";
                    echo "</tr>";
                }
            } else {
                echo "<tr><td colspan='2'>沒有找到任何數據.</td></tr>";
            }
        }
        ?>
    </table>
</body>
</html>
<?php
// 關閉數據庫連接
$conn->close();
?>
