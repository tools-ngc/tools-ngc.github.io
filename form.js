
// window.onload = function()
// {
// 	document.getElementById("button").onclick = function(){
// 		getDarpaListings();
// 	};
// }

	

// function doWork(params) {
// 	$.get("get_new_program_managers",function(data){
// 		var test_data = '';
// 		$.each(data, function(index, value){
// 			test_data += '<tr>';
// 			test_data += '<td>' + value.name + '</td>'
// 			test_data += '<td>' + value.office + '</td>'
// 			test_data += '</tr>';
// 		});
// 		$('table').append(test_data);
		
// 	});
// 	event.preventDefault()
// }

// function getDarpaListings()
// {
// 	$.get("get_darpa_listings", function(data){
// 		var test_data = '';
// 		$.each(data, function(index,value){
// 			console.log(value.contractname)
// 			test_data += '<tr>';
// 			test_data += '<td>' + value.contractname + '</td>'
// 			test_data += '<td>' + value.noticeid + '</td>'
// 			test_data += '<td>' + value.currentresponsedate + '</td>'
// 			test_data += '<td>' + value.lastupdateddate + '</td>'
// 			test_data += '<td>' + value.lastpublisheddate + '</td>'
// 			test_data += '<td>' + value.type + '</td>'
// 			test_data += '<td>' + value.url + '</td>'
// 			test_data += '</tr>';
// 		});
// 		$('table').append(test_data);
// 	});
// 	event.preventDefault()
// }

$(document).ready(function() {

	$.getJSON("https://tools-ngc.github.io/DARPA.json", function(json) {
		console.log(json); // this will show the info it in firebug console
	});


	$('#table').DataTable({
			processing : true,
			responsive : true,
			language: {
				'loadingRecords': '&nbsp;',
			},                
			ajax:{
				url:'/api/get_darpa_listings',
				method: "GET",
				dataSrc: ''
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
			url:'/api/get_new_program_managers',
			method: "GET",
			dataSrc: ''
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
		url:'/api/get_MTO_program_managers',
		method: "GET",
		dataSrc: ''
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
		url:'/api/get_I2O_program_managers',
		method: "GET",
		dataSrc: ''
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
		url:'/api/get_BTO_program_managers',
		method: "GET",
		dataSrc: ''
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
		url:'/api/get_STO_program_managers',
		method: "GET",
		dataSrc: ''
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
		url:'/api/get_TTO_program_managers',
		method: "GET",
		dataSrc: ''
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
		url:'/api/get_DSO_program_managers',
		method: "GET",
		dataSrc: ''
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

	
