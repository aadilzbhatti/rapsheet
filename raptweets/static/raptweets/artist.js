/**
 * Created by aadil on 11/28/15.
 */

$(document).ready(function() {
    var $work = $('#data');
    var $data = JSON.parse($work.text());
    $work.empty();
    console.log($data);
});