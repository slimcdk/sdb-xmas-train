


fn = 30;



difference() {

    union() {

        difference () {
            linear_extrude(40) circle(d=32, $fn=fn);
            linear_extrude(40) circle(d=24.7, $fn=6);
        }
        
        translate([0,0,40]) difference() {
            linear_extrude(12) circle(d=60, $fn=fn);
            linear_extrude(12) circle(d=9, $fn=fn);
            translate([0,0,6]) linear_extrude(6) circle(d=20, $fn=fn);
        }
    }
    
    hs = 45/2;
    #translate([0,0,40]) for (i = [0:5]) {
        echo(360*i/6, sin(360*i/6)*hs, cos(360*i/6)*hs);
        translate([sin(360*i/6)*hs, cos(360*i/6)*hs, 0 ])
        cylinder(h = 12, d=6, $fn=fn);
    }
    
}