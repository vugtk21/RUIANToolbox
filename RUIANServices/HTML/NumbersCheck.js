function isNumber(event, scope, numDigits, maxValue)
{
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
 
 return true;
}