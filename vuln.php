<?php

/*Update with your test database information*/
$servername = "192.168.1.92";
$username = "testuser";
$password = "testuserpass";
$dbname = "sampledb";

    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if(isset($_GET['vulnfield'])){
    $sql = "insert into employees values('" . $_GET['vulnfield']  ."',curdate(),'fname','lname','M',curdate())";
    $conn->exec($sql);
    }


?>
