JSCODE = '''

function abcd1(_0x17164c) {
    return abcd2(_0x17164c, 3597397);
}
//var rndnum = "1862457550.55374328";
//var starttime = "2021/1/26 13:01:53";
//var activityId = '104530885';
function abcd2(_0x1b1e02, _0x23f273) {
    var _0x1f9ba1 = 2147483648;
    var _0x3b83ae = 2147483647;

    var _0x4ad458 = ~~(_0x1b1e02 / _0x1f9ba1);

    var _0x470088 = ~~(_0x23f273 / _0x1f9ba1);

    var _0x5bc159 = _0x1b1e02 & _0x3b83ae;

    var _0x35dfa5 = _0x23f273 & _0x3b83ae;

    var _0x353774 = _0x4ad458 ^ _0x470088;

    var _0x4a742c = _0x5bc159 ^ _0x35dfa5;

    return _0x353774 * _0x1f9ba1 + _0x4a742c;
}

function abcd3(data1, data2) {
    if (data1 - 62 < 0) {
        var data3 = data2.substr(data1, 1);
        return data3;
    }

    var _0x45571c = data1 % 62;

    var _0x4e6181 = parseInt(data1 / 62);

    return abcd3(_0x4e6181, data2) + data2.substr(_0x45571c, 1);
}

function abcd4(_0x11dbf0, _0x1558df) {


    var _0x556c7b = _0x1558df.split("");

    var _0x27312b = _0x1558df.length;

    for (var _0x107cfb = 0; _0x107cfb < _0x11dbf0.length; _0x107cfb++) {
        var _0x410c33 = parseInt(_0x11dbf0[_0x107cfb]);

        var _0x43a652 = _0x556c7b[_0x410c33];
        var _0x433a77 = _0x556c7b[_0x27312b - 1 - _0x410c33];
        _0x556c7b[_0x410c33] = _0x433a77;
        _0x556c7b[_0x27312b - 1 - _0x410c33] = _0x43a652;
    }

    _0x1558df = _0x556c7b.join("");
    return _0x1558df;
}

function abcd5(_0x5565b6) {


    var _0x546e81 = 0;

    var _0x5ed7b1 = _0x5565b6.split("");

    for (var _0x28a6c3 = 0; _0x28a6c3 < _0x5ed7b1.length; _0x28a6c3++) {
        _0x546e81 += _0x5ed7b1[_0x28a6c3].charCodeAt();
    }

    var _0x5af006 = _0x5565b6.length;

    var _0x5258e0 = _0x546e81 % _0x5af006;

    var _0x2b24c5 = [];

    for (var _0x28a6c3 = _0x5258e0; _0x28a6c3 < _0x5af006; _0x28a6c3++) {
        _0x2b24c5.push(_0x5ed7b1[_0x28a6c3]);
    }

    for (var _0x28a6c3 = 0; _0x28a6c3 < _0x5258e0; _0x28a6c3++) {
        _0x2b24c5.push(_0x5ed7b1[_0x28a6c3]);
    }

    return _0x2b24c5.join("");
}

function abcdu(_0x92722d) {
    var _0x2eb3ad = -480;

    var _0x3a4ef4 = new Date().getTimezoneOffset();

    var _0x58cdae = _0x2eb3ad - _0x3a4ef4;

    return _0x92722d.getTime() / 1000 + _0x58cdae * 60;
}
function getcanshu(rndnum,starttime,activityId){

var _0x3098bf = rndnum.split(".")[0];

var _0x4aaf4a = abcd1(parseInt(_0x3098bf));

var _0x149db2 = (_0x4aaf4a + "").split("");

var _0x5b9ae2 = starttime || window.initstime;

var _0x4eae39 = abcdu(new Date(_0x5b9ae2.replace(new RegExp("-", "gm"), "/")));

var _0x5050a2 = _0x4eae39 + "";

if (_0x4eae39 % 10 > 0) {
    _0x5050a2 = _0x5050a2.split("").reverse().join("");
}

var _0xd16fcc = parseInt(_0x5050a2 + "89123");

var _0x149db2 = (_0xd16fcc + "" + (_0x4aaf4a + "")).split("");

var _0x1b3de6 = abcd4(_0x149db2, "kgESOLJUbB2fCteoQdYmXvF8j9IZs3K0i6w75VcDnG14WAyaxNqPuRlpTHMrhz");

var _0x3a5cf2 = _0xd16fcc + _0x4aaf4a + parseInt(activityId);

jqParam = abcd3(_0x3a5cf2, _0x1b3de6);

var _0x5d90fd = abcd5(jqParam);

jqParam = _0x5d90fd;

return jqParam
}
'''
