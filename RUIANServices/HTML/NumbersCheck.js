function isNumber(event, scope, numDigits, maxValue)
{
 if ((event.isChar == undefined) || (event.isChar)) {
    value = scope.value +  String.fromCharCode(event.charCode);
    numValue = Number(value);
 
    if (isNaN(value)) {
	    return false;
    }

    if ( (numDigits > 0) && (value.length > numDigits) ) {
	    return false;
    }

    if ( (maxValue > 0) && (numValue > maxValue)) {
	    return false;
    }
 }
 
 return true;
}

function isENLetter(event, scope)
{
 if ((event.isChar == undefined) || (event.isChar)) {
    value = scope.value +  String.fromCharCode(event.charCode);
    if (scope.value != "") {
       return (value == "ch") || (value == "CH");
    }
    else {
        charStr = String.fromCharCode(event.charCode);
        return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".indexOf(charStr) != -1;
    }
 }

 return true;
}
