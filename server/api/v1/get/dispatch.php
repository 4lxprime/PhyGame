<?php

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");

?>

<?php

include '../db/db_conn.php';

$sql="SELECT * FROM servers";
$result=mysqli_query($conn, $sql);

if (mysqli_num_rows($result)!=0) {
    $row=mysqli_fetch_all($result, MYSQLI_ASSOC);
    echo json_encode($row, JSON_PRETTY_PRINT);

} else {

    echo json_encode("error", JSON_PRETTY_PRINT);

}

?>