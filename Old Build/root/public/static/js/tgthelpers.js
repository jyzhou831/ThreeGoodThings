function relativeDate(olderDate) {
  if (typeof olderDate == "string") olderDate = new Date(olderDate);
  var now = new Date(),
  	  //milliseconds = new Date(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds()) - olderDate,
  	  milliseconds = now - olderDate,
  	  conversions = [
		["yrs", 31518720000],
		["mon", 2626560000],
		["days", 86400000],
		["hrs", 3600000],
		["min", 60000],
		["sec", 1000]
	  ];
	  
  for (var i = 0; i<conversions.length; i++) {
    var result = Math.floor(milliseconds / conversions[i][1]);
    if (result >= 2) {
      return result + " " + conversions[i][0];
    }
  }
  return "just now";
};
