$(document).ready(function() {

    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var success_msg = function(statement){
        var div = $("#warning");
        div.removeClass('hide alert-danger');
        div.addClass('alert-success');
        var span = $('#warning span').first();
        span.removeClass('glyphicon-exclamation-sign');
        span.addClass('glyphicon-ok-sign');
        span.next('span').text('Success! '+ statement);
    };

    var warning = function(statement){
        var div = $("#warning");
        div.removeClass('hide alert-success');
        div.addClass('alert-danger');
        var span = $('#warning span').first();
        span.removeClass('glyphicon-ok-sign');
        span.addClass('glyphicon-exclamation-sign');
        span.next('span').text('Warning! ' + statement);
    };

    var deposit_warning = function() {
        $("#deposit_warning").removeClass('hide');
    };

    var act_map = {}
    var show_table = function(user_ac){
        // try cache or send request
        var act = act_map[user_ac.ac_id];
        if (typeof act === 'undefined') {
            $.ajax({
                type: "GET",
                url: "/get/activity",
                async: false,
                data: {'id':user_ac.ac_id},
                success: function(result) {
                    result = result[0];
                    act = result.fields;
                    act_map[user_ac.ac_id] = act;
                }
            });
        }
        $(".table").append(
            '<tr class="tmp_table" name="'+user_ac.ac_id+'">'+
                '<td class="table-id-code"><button type="button" class="close" aria-label="Close"><span aria-hidden="true">&times;</span></button></td>'+
                '<td class="table-date-time" name="time">'+user_ac.date+' '+user_ac.time+'</td>'+
                '<td>'+act.name+'('+act.during_time+')'+'</td>'+
                '<td class="table-money">'+act.web_adult+'</td>'+
                '<td class="table-money">'+act.web_child+'</td>'+
                '<td class="table-money">'+act.KTL_adult+'</td>'+
                '<td class="table-money">'+act.KTL_child+'</td>'+
                '<td><input class="count" type="text" name="ad_count" value="0" style="width: 20px; text-align: right"></td>'+
                '<td><input class="count" type="text" name="ch_count" value="0" style="width: 20px; text-align: right"></td>'+
                '<td class="table-money" name="sub_total">0.00</td>'+
                '<td class="table-money" name="sub_nopay_total">0.00</td>'+
            '</tr>'
        );
    };

    var check_detail_name = function() {
        var input=$(this);
        var is_name=input.val()
        if(is_name){
            input.parent().removeClass("has-error").addClass("has-success");
            input.next('span').removeClass("error_show").addClass("error");
        }
        else{
            input.parent().removeClass("has-success").addClass("has-error");
            input.next('span').removeClass("error").addClass("error_show");
        }
    };

    $('#email').on('input', function() {
        var input=$(this);
        var re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
        var is_email=re.test(input.val());
        if(is_email){
            input.parent().removeClass("has-error").addClass("has-success");
            input.next('span').removeClass("error_show").addClass("error");
        }
        else{
            input.parent().removeClass("has-success").addClass("has-error");
            input.next('span').removeClass("error").addClass("error_show");
        }
    });



    $("#location").on("change", function() {
        $("#ac_name").find("optgroup.tmp_list").remove().end();
        $("#ac_name").find("option.tmp_list").remove().end();

        $.get("/get/activities",{'location_id': $(this).val()})
            .done(function(act_list){
            var map = {};
            for (var i = 0; i < act_list.length; i++) {
                var company = act_list[i].company;
                if (company in map == false){
                    var id = 'optg' + i;
                    map[company] = id
                    $("#ac_name").append('<optgroup id="'+id+'" class="tmp_list" label="'+company+'"></optgroup>');
                }
                $("#"+map[company]).append('<option class="tmp_list" value='+act_list[i].id+">"+act_list[i].name+"</option>" );
            };
        });
    });

    $("#ac_name").on("change", function() {
        $("#time").find("option.tmp_list").remove().end();
        $.get("/get/timetable",{'id': $(this).val()})
            .done(function(time_table){
            for (var i = 0; i < time_table.length; i++) {
                $("#time").append('<option class="tmp_list" value='+i+">"+time_table[i]+"</option>" );
            };
        });
    });

    $("#join").click(function(){
        $a = $('#ac_name option.tmp_list');
        if ($a.is($a) == false){
            warning('請選擇地點。');
            return;
        }
        var check_activity = false
        $a.each(function() {
            if ($(this).is(':selected') == false){
                return;
            }
            check_activity = true
            var date = $("#date").val();
            if (date == ''){
                warning('請選擇日期。');
                return false;
            }
            var user_ac = {
                "date": $("#date").val(),
                "time": $("#time option.tmp_list:selected").text(),
                "ac_id": $("#ac_name").val(),
                };
            show_table(user_ac);
            success_msg('成功加入活動。');
            return false;
        })
        if (!check_activity){warning('請選擇活動。');}
    })

    var recount = function(){
        var deposit = false;
        var sub_all = 0;
        var to_pay = 0;
        var all_total = 0;
        var all_to_pay = 0;
        var ad_count = 0;
        var ch_count = 0;
        for (var i = 1; i <= $("tr.tmp_table").length; i++) {
            $tmp_tr = $(".table").find("tr:nth-child("+(i+2)+")");
            var ac_id = $tmp_tr.attr('name');
            var act = act_map[ac_id];
            ad_count = $tmp_tr.find("[name='ad_count']").val();
            ch_count = $tmp_tr.find("[name='ch_count']").val();
            sub_all = ad_count * act.KTL_adult + ch_count * act.KTL_child
            all_total = all_total + sub_all
            if (!act.deposit){ // 全額預付
                to_pay = sub_all;
            }
            else{ // 預付訂金
                deposit = true
                to_pay = ad_count * act.deposit_adult + ch_count * act.deposit_child
            }
            $tmp_tr.find("[name='sub_total']").text(to_pay.toFixed(2));
            $tmp_tr.find("[name='sub_nopay_total']").text((sub_all - to_pay).toFixed(2));

            all_to_pay = all_to_pay + to_pay;
        };
        $("#all_total").text(all_total.toFixed(2));
        $("#pay_total").text(all_to_pay.toFixed(2));
        $("#no_pay_total").text((all_total - all_to_pay).toFixed(2));

        if (deposit) {
            deposit_warning()
        }
    }

    var detail_check_before_submit = function(event){
        var form_data=$("#p_detail");
        var error_free=true;
        form_data.children('div').each(function(){
            var error = $(this).hasClass("has-error");
            var error_element=$(this).find("span");
            if (error){error_element.removeClass("error").addClass("error_show"); error_free=false;}
            else {
              error_element.removeClass("error_show").addClass("error");
            }
        })
        if (!error_free){
            alert('請填寫基本資料。');
            return;
        }

        var p_detail = {
            title: $("#title option:selected").text(),
            last_name: $("#last_name").val(),
            first_name: $("#first_name").val(),
            email: $("#email").val(),
            phone: $("#phone").val(),
        }
        var activities = new Array();
        $("table tr.tmp_table").each(function(){
            var activity = {
                id: $(this).attr('name'),
                time: $(this).find("[name='time']").text(),
                ad_count: $(this).find("[name='ad_count']").val(),
                ch_count: $(this).find("[name='ch_count']").val(),
            }
            activities.push(activity)
        })

        $.ajax({
            type: "POST",
            url: "/post/booking/",
            data: JSON.stringify({'detail': p_detail, 'activities': activities}),
            success: function(data){alert(data+' 請儘快與您的旅遊經紀人聯繫');},
            failure: function(errMsg) {alert(errMsg);}
        });
    };

    $('#last_name').on('input', check_detail_name);
    $('#first_name').on('input', check_detail_name);
    $('#phone').on('input', check_detail_name);

    $('#send').on('click', detail_check_before_submit)
    $(document).on('click', 'button.close', function () { // <-- changes
        $(this).closest('tr').remove();
    });
    $(document).on('keyup', 'input.count', recount);
    $(document).on('click', 'input.count', function(){
        $(this).select()
    });
});
