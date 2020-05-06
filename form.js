
$(document).ready(function() {

	/* var url="https://tools-ngc.github.io/DARPA.json";
	$.getJSON(url, function (data) {
		for(var item in data.mto) {
			alert(JSON.stringify(data.mto[item]));
		}
	}); */




 	 $('#table').DataTable({
			processing : true,
			responsive : true,
			language: {
				'loadingRecords': '&nbsp;',
			},                
			ajax:{
				url:'https://tools-ngc.github.io/DARPA.json',
				method: "GET",
				dataSrc: function(json){
					var item , data = [];
					for(var listing in json.darpa_listings){
						item = (json.darpa_listings[listing]);
						data.push(item);
					}
					return data
				}
			},
			dom: 'Bfrtip',
			order:[3,"desc"],
			columns:[
							{data: "contractname",
									fnCreatedCell: function(nTd, sData, oData, iRow, iCol){
											$(nTd).html("<a class=changeColor href='" + oData.url+"' target='_blank'>" + oData.contractname+"</a>")
								
									}
							},
							{data: "noticeid"},
							{data: "proposalduedate"},
							{data: "lastupdateddate"},
							{data: "lastpublisheddate"},
							{data: "type"},
							{data: "awardee"},
							{data: "contractValue"},
							{data: "importantDates"}
					],
			
			"fnRowCallback" : function(row, data, dataIndex){
				if(data['color'] == "red"){
					$(row).css('background-color','red');
				}
				if(data['color'] == "green"){
					$(row).css('background-color','green');
				}
				if(data['color'] == "yellow"){
					$(row).css('background-color','yellow');
				}
			},

			buttons: [
				{
					text: 'Reload',
					action: function(e, dt, node, config)
					{	
						dt.ajax.reload();
					}
				}
			]
	});	
 

	$('#tableProgramManagers').DataTable({
		processing : true,
		responsive : true,
		language: {
			'loadingRecords': '&nbsp;',
		},                
		ajax:{
			url:'https://tools-ngc.github.io/DARPA.json',
			method: "GET",
			dataSrc: function(json){
				var item , data = [];
				for(var listing in json.new_program_managers){
					item = (json.new_program_managers[listing]);
					data.push(item);
				}
				return data
			}
		},
		dom: 'Bfrtip',
		columns:[
						{data: "name"},
						{data: "office"},
						{data: "description"},
						{data: "interests"},
						{data: "programs"}
						],
		buttons: [
			{
				text: 'Reload',
				action: function(e, dt, node, config)
				{	
					dt.ajax.reload();
				}
			}
		]
});	



$('#tableMTOProgramManagers').DataTable({
	processing : true,
	responsive : true,
	language: {
		'loadingRecords': '&nbsp;',
	},                
	ajax:{
		url:'https://tools-ngc.github.io/DARPA.json',
		method: "GET",
		dataSrc: function(json){
			var item , data = [];
			for(var listing in json.mto){
				item = (json.mto[listing]);
				data.push(item);
			}
			return data
		}
	},
	dom: 'Bfrtip',
	columns:[
					{data: "name"},
					{data: "title"},
					{data: "description"},
					{data: "interests"},
					{data: "programs"}
					],
	buttons: [
		{
			text: 'Reload',
			action: function(e, dt, node, config)
			{	
				dt.ajax.reload();
			}
		}
	]
});	

$('#tableI2OProgramManagers').DataTable({
	processing : true,
	responsive : true,
	language: {
		'loadingRecords': '&nbsp;',
	},                
	ajax:{
		url:'https://tools-ngc.github.io/DARPA.json',
		method: "GET",
		dataSrc: function(json){
			var item , data = [];
			for(var listing in json.i2o){
				item = (json.i2o[listing]);
				data.push(item);
			}
			return data
		}
	},
	dom: 'Bfrtip',
	columns:[
					{data: "name"},
					{data: "title"},
					{data: "description"},
					{data: "interests"},
					{data: "programs"}
					],
	buttons: [
		{
			text: 'Reload',
			action: function(e, dt, node, config)
			{	
				dt.ajax.reload();
			}
		}
	]
});	



$('#tableBTOProgramManagers').DataTable({
	processing : true,
	responsive : true,
	language: {
		'loadingRecords': '&nbsp;',
	},                
	ajax:{
		url:'https://tools-ngc.github.io/DARPA.json',
		method: "GET",
		dataSrc: function(json){
			var item , data = [];
			for(var listing in json.bto){
				item = (json.bto[listing]);
				data.push(item);
			}
			return data
		}
	},
	dom: 'Bfrtip',
	columns:[
					{data: "name"},
					{data: "title"},
					{data: "description"},
					{data: "interests"},
					{data: "programs"}
					],
	buttons: [
		{
			text: 'Reload',
			action: function(e, dt, node, config)
			{	
				dt.ajax.reload();
			}
		}
	]
});	


$('#tableSTOProgramManagers').DataTable({
	processing : true,
	responsive : true,
	language: {
		'loadingRecords': '&nbsp;',
	},                
	ajax:{
		url:'https://tools-ngc.github.io/DARPA.json',
		method: "GET",
		dataSrc: function(json){
			var item , data = [];
			for(var listing in json.sto){
				item = (json.sto[listing]);
				data.push(item);
			}
			return data
		}
	},
	dom: 'Bfrtip',
	columns:[
					{data: "name"},
					{data: "title"},
					{data: "description"},
					{data: "interests"},
					{data: "programs"}
					],
	buttons: [
		{
			text: 'Reload',
			action: function(e, dt, node, config)
			{	
				dt.ajax.reload();
			}
		}
	]
});	


$('#tableTTOProgramManagers').DataTable({
	processing : true,
	responsive : true,
	language: {
		'loadingRecords': '&nbsp;',
	},                
	ajax:{
		url:'https://tools-ngc.github.io/DARPA.json',
		method: "GET",
		dataSrc: function(json){
			var item , data = [];
			for(var listing in json.tto){
				item = (json.tto[listing]);
				data.push(item);
			}
			return data
		}
	},
	dom: 'Bfrtip',
	columns:[
					{data: "name"},
					{data: "title"},
					{data: "description"},
					{data: "interests"},
					{data: "programs"}
					],
	buttons: [
		{
			text: 'Reload',
			action: function(e, dt, node, config)
			{	
				dt.ajax.reload();
			}
		}
	]
});	



$('#tableDSOProgramManagers').DataTable({
	processing : true,
	responsive : true,
	language: {
		'loadingRecords': '&nbsp;',
	},                
	ajax:{
		url:'https://tools-ngc.github.io/DARPA.json',
		method: "GET",
		dataSrc: function(json){
			var item , data = [];
			for(var listing in json.dso){
				item = (json.dso[listing]);
				data.push(item);
			}
			return data
		}
	},
	dom: 'Bfrtip',
	columns:[
					{data: "name"},
					{data: "title"},
					{data: "description"},
					{data: "interests"},
					{data: "programs"}
					],
	buttons: [
		{
			text: 'Reload',
			action: function(e, dt, node, config)
			{	
				dt.ajax.reload();
			}
		}
	]
});	 





});

	
