//★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
// CSRFトークンに関する処理
//★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
// HTMLロード直後に動作
//★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
$(window).on('pageshow', function(){
    //---------------------------------------------------------------------------------
    // 開始日の祝、土、日に色を付ける
    //---------------------------------------------------------------------------------
    var cities = $('#id_f_s_day').children();
    for (var i=0; i<cities.length; i++) {
        var string = cities.eq(i).text();
        if(string.indexOf('祝') > -1){
            cities[i].classList.add('cl-dark-holiday');
            cities[i].textContent = string.replace('祝', '');
        } else if(string.indexOf('日') > -1){
            cities[i].classList.add('cl-dark-holiday');
        } else if(string.indexOf('土') > -1){
            cities[i].classList.add('cl-dark-saturday');
        }
    }

    //---------------------------------------------------------------------------------
    // 終了日の祝、土、日に色を付ける　※存在する場合のみ
    //---------------------------------------------------------------------------------
    if($('#id_f_e_day').length){
        var cities = $('#id_f_e_day').children();
        for (var i=0; i<cities.length; i++) {
            var string = cities.eq(i).text();
            if(string.indexOf('祝') > -1){
                cities[i].classList.add('cl-dark-holiday');
                cities[i].textContent = string.replace('祝', '');
            } else if(string.indexOf('日') > -1){
                cities[i].classList.add('cl-dark-holiday');
            } else if(string.indexOf('土') > -1){
                cities[i].classList.add('cl-dark-saturday');
            }
        }
    }

    //---------------------------------------------------------------------------------
    // 予定タグの色作成
    //---------------------------------------------------------------------------------
    var tag_wk = {};
    // 設定値退避
    var cities = $('#id_f_tag').children();
    for (var i=0; i<cities.length; i++) {
        tag_wk[cities.eq(i).val()] = cities.eq(i).text();
    }

    // 全て取り除いて再設定
    $('#id_f_tag > option').remove();
    for (var key in tag_wk) {
        if(tag_wk[key].indexOf('#') > -1){
            let disp_text = tag_wk[key].split(",");
            $("#id_f_tag").append("<option value=" + key + " style='background-color:" + disp_text[0] + ";'>" + disp_text[1] + "</option>");
        } else {
            $("#id_f_tag").append("<option value=" + key + ">" + tag_wk[key] + "</option>");
        }
    }
});

//★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
// 通常時
//★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
$(function($) {
//---------------------------------------------------------------------------------
// 日の祝、土、日に色を付ける
//---------------------------------------------------------------------------------
function combo_id_f_day_add_color(id_name) {
    var cities = $(id_name).children();
    for (var i=0; i<cities.length; i++) {
        var string = cities.eq(i).text();
        if(string.indexOf('祝') > -1){
            cities[i].classList.add('cl-dark-holiday');
            cities[i].textContent = string.replace('祝', '');
        } else if(string.indexOf('日') > -1){
            cities[i].classList.add('cl-dark-holiday');
        } else if(string.indexOf('土') > -1){
            cities[i].classList.add('cl-dark-saturday');
        }
    }
}

//---------------------------------------------------------------------------------
// コンボボックスに指定したValueが存在するかチェック
//---------------------------------------------------------------------------------
function is_option_value(id_name, value) {
    var cities = $(id_name).children();
    for (var i=0; i<cities.length; i++) {
        if(cities.eq(i).val() == value) {
            return true;
        }
    }
    return false;
}

//---------------------------------------------------------------------------------
// グループコンボボックス更新　※①(検索結果)追加、②(検索結果)削除
//---------------------------------------------------------------------------------
function combo_id_f_member_gr_chg(add_flg) {
    // 設定値退避
    var gr_wk = {};
    var gr_select = $('#id_f_member_gr').val();
    var cities = $('#id_f_member_gr').children();
    for (var i=0; i<cities.length; i++) {
        gr_wk[cities.eq(i).val()] = cities.eq(i).text();
    }

    // 全て取り除いて再設定
    $('#id_f_member_gr > option').remove();
    if(add_flg == true) {
        $("#id_f_member_gr").append("<option value=0>(検索結果)</option>");
        gr_select = "(検索結果)";
    }
    for (var key in gr_wk) {
        if(gr_wk[key].indexOf('検索結果') > -1){
            // なにもしない（削除）
        } else {
            $("#id_f_member_gr").append("<option value=" + key + ">" + gr_wk[key] + "</option>");
        }
    }
    if(gr_select != "(検索結果)") {
        $("#id_f_member_gr").val(gr_select);
    }
}

//---------------------------------------------------------------------------------
// 年、月コンボボックス変更時、日データ取得
//---------------------------------------------------------------------------------
function ajax_disp_days(year, month, id_name) {
    // Ajax通信
    $.ajax({
        'url': g_url_ajax_get_days,
        'type': 'GET',
        'data': {
            'year': year,
            'month': month,
        },
        'dataType': 'json'
    }).done( function(data) {
        // 変換
        const days_list = JSON.parse(data);

        // 全て取り除いて再設定
        $(id_name + ' > option').remove();
        $.each(days_list, function(index, value){
            $(id_name).append($('<option>').html(value[1]).val(value[0]));
        });
        combo_id_f_day_add_color(id_name);
    })
    .fail(function() {
        alert("日データの取得に失敗しました。");
    });
}
// Changeイベント
$('#id_f_s_year').change(function() {
    const year = $('#id_f_s_year').val();
    const month = $('#id_f_s_month').val();
    ajax_disp_days(year, month, '#id_f_s_day');
});
// Changeイベント
$('#id_f_s_month').change(function() {
    const year = $('#id_f_s_year').val();
    const month = $('#id_f_s_month').val();
    ajax_disp_days(year, month, '#id_f_s_day');
});

//---------------------------------------------------------------------------------
// グループコンボボックス変更時、グループデータ取得
//---------------------------------------------------------------------------------
$('#id_f_member_gr').change(function() {
    // 変更後のグループ取得
    const chg_group = $('#id_f_member_gr').val();

    // Ajax通信
    $.ajax({
        'url': g_url_ajax_get_getgrs,
        'type': 'GET',
        'data': {
            'group': chg_group,
        },
        'dataType': 'json'
    }).done( function(data) {
        // 変換
        const gr_list = JSON.parse(data);

        // グループコンボボックス更新
        combo_id_f_member_gr_chg(false);

        // 全て取り除いて再設定
        $('#id_f_member_r > option').remove();
        $.each(gr_list, function(index, value){
            $('#id_f_member_r').append($('<option>').html(value[1]).val(value[0]));
        });
    })
    .fail(function() {
        alert("グループデータの取得に失敗しました。");
    });
});

//---------------------------------------------------------------------------------
// 施設コンボボックス変更時、施設データ取得
//---------------------------------------------------------------------------------
$('#id_f_setu_gr').change(function() {
    // 変更後の施設取得
    const chg_group = $('#id_f_setu_gr').val();

    // Ajax通信
    $.ajax({
        'url': g_url_ajax_get_getsisetus,
        'type': 'GET',
        'data': {
            'group': chg_group,
        },
        'dataType': 'json'
    }).done( function(data) {
        // 変換
        const gr_list = JSON.parse(data);

        // 全て取り除いて再設定
        $('#id_f_setu_r > option').remove();
        $.each(gr_list, function(index, value){
            $('#id_f_setu_r').append($('<option>').html(value[1]).val(value[0]));
        });
    })
    .fail(function() {
        alert("施設データの取得に失敗しました。");
    });
});

//---------------------------------------------------------------------------------
// アカウント検索コンボボックス変更時、検索結果データ取得
//---------------------------------------------------------------------------------
$('#AddressSearch').on('click', function() {
    // 入力値取得
    const imput_text = $('#AddressSearchText').val();
    if(imput_text == ""){
        alert("検索文字列を入力してください。");
        return;
    }

    // Ajax通信
    $.ajax({
        'url': g_url_ajax_get_accounts,
        'type': 'GET',
        'data': {
            'search': imput_text,
        },
        'dataType': 'json'
    }).done( function(data) {
        // 変換
        const account_list = JSON.parse(data);

        // グループコンボボックス更新
        combo_id_f_member_gr_chg(true);

        // 全て取り除いて再設定
        $('#id_f_member_r > option').remove();
        $.each(account_list, function(index, value){
            $('#id_f_member_r').append($('<option>').html(value[1]).val(value[0]));
        });
    })
    .fail(function() {
        alert("検索結果データ取得に失敗しました。");
    });
});

//---------------------------------------------------------------------------------
// 参加者：追加／削除
//---------------------------------------------------------------------------------
$('#member_add').on('click', function() {
    // 選択値取得
    $('#id_f_member_r option:selected').each(function() {
        if(is_option_value('#id_f_member_l', $(this).val()) == true) {
            // 存在するときはなにもしない
        } else {
            $('#id_f_member_l').append($('<option>').html($(this).text()).val($(this).val()));
        }
    });
});
$('#member_del').on('click', function() {
    // 選択値取得
    $('#id_f_member_l option:selected').each(function() {
        // 削除
        $('#id_f_member_l').children("option[value='" + $(this).val() + "']").remove();
    });
});

//---------------------------------------------------------------------------------
// 施設：追加／削除
//---------------------------------------------------------------------------------
$('#setu_add').on('click', function() {
    // 選択値取得
    $('#id_f_setu_r option:selected').each(function() {
        if(is_option_value('#id_f_setu_l', $(this).val()) == true) {
            // 存在するときはなにもしない
        } else {
            $('#id_f_setu_l').append($('<option>').html($(this).text()).val($(this).val()));
        }
    });
});
$('#setu_del').on('click', function() {
    // 選択値取得
    $('#id_f_setu_l option:selected').each(function() {
        // 削除
        $('#id_f_setu_l').children("option[value='" + $(this).val() + "']").remove();
    });
});

//---------------------------------------------------------------------------------
// スケジュール登録ボタン
//---------------------------------------------------------------------------------
$('#sch_regist').on('click', function() {
    // 終了日が存在する場合
    if($('#id_f_e_year').length){
        let s_year = $('#id_f_s_year').val();
        let s_month = $('#id_f_s_month').val();
        let s_day = $('#id_f_s_day').val();
        let chk_s_date = new Date(Number(s_year), Number(s_month), Number(s_day));
        let e_year = $('#id_f_e_year').val();
        let e_month = $('#id_f_e_month').val();
        let e_day = $('#id_f_e_day').val();
        let chk_e_date = new Date(Number(e_year), Number(e_month), Number(e_day));
        // 日付前後チェック
        if(chk_s_date > chk_e_date) {
            alert("終了日は開始日以降に設定してください。");
            return false;
        }
        // 時間前後チェック
        if(s_date == e_date) {
            // 時刻が存在する場合
            if($('#id_f_s_hour').length){
                var s_hour = $('#id_f_s_hour').val();
                var s_minute = $('#id_f_s_minutes').val();
                var e_hour = $('#id_f_e_hour').val();
                var e_minute = $('#id_f_e_minutes').val();
                if( s_hour != 98 && s_hour != 99 && e_hour != 98 && e_hour != 99 && s_minute != 99 && e_minute != 99) {
                    let chk_s_time = new Date(1900, 1, 1, Number(s_hour), Number(s_minute), 0);
                    let chk_e_time = new Date(1900, 1, 1, Number(e_hour), Number(e_minute), 0);
                   // 時間前後チェック
                    if(chk_s_time > chk_e_time) {
                        alert("終了時刻は開始時刻以降に設定してください。");
                        return false;
                    }
                }
            }
        }
    }
    else {
        // 時間前後チェック
        var s_hour = $('#id_f_s_hour').val();
        var s_minute = $('#id_f_s_minutes').val();
        var e_hour = $('#id_f_e_hour').val();
        var e_minute = $('#id_f_e_minutes').val();
        if( s_hour != 98 && s_hour != 99 && e_hour != 98 && e_hour != 99 && s_minute != 99 && e_minute != 99) {
            let chk_s_time = new Date(1900, 1, 1, Number(s_hour), Number(s_minute), 0);
            let chk_e_time = new Date(1900, 1, 1, Number(e_hour), Number(e_minute), 0);
            // 時間前後チェック
            if(chk_s_time > chk_e_time) {
                alert("終了時刻は開始時刻以降に設定してください。");
                return false;
            }
        }
    }

    // 参加者を選択状態にする　※選択しておかないとViewで取得できない
    $('#id_f_member_l option').prop('selected', true);
    // 施設を選択状態にする　※選択しておかないとViewで取得できない
    $('#id_f_setu_l option').prop('selected', true);
});

// function終端
});
