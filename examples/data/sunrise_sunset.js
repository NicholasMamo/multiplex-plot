/*
 * Code to collect sunrise and sunset times from https://www.timeanddate.com/sun/malta/valletta
 */

var jq = document.createElement('script');
jq.src = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(jq);
jQuery.noConflict();
month = jQuery('[name="month"]').val();
year = jQuery('[name="year"]').val()

sunrise = [];
sunset = [];
$$("#as-monthsun tr").slice(3, -1).forEach((element, index) => {
    data = jQuery(element).find('td').slice(0, 2);
    if (jQuery(element).find('th').length) { 
        day = jQuery(element).find('th')[0].innerText;
        sunrise.push({ 'month': month, 'year': year, 'day': day, 'time': data[0].innerText.substring(0, 5) });
        sunset.push({ 'month': month, 'year': year, 'day': day, 'time': data[1].innerText.substring(0, 5) });
    }
});
console.log(sunrise);
console.log(sunset);
copy(sunrise)