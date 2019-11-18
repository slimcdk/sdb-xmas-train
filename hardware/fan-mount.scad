


fn = 30;
base_thickness = 3;
bolt_d = 2.9;

difference() {
    union() {
        difference() {
            linear_extrude(base_thickness) square(size=[50, 55]);
            
            translate([25,25]) {
                linear_extrude(base_thickness) circle(d=46, $fn=fn);

                translate([20, 20]) linear_extrude(base_thickness) circle(d=3, $fn=fn);
                translate([-20, 20]) linear_extrude(base_thickness) circle(d=3, $fn=fn);
                translate([20, -20]) linear_extrude(base_thickness) circle(d=3, $fn=fn);
                translate([-20, -20]) linear_extrude(base_thickness) circle(d=3, $fn=fn);
            }
        }
        translate([25,25]) {
            linear_extrude(base_thickness) circle(d=25, $fn=fn);
            
            for (i = [0:120:360]){
                rotate(i,0,0) translate([0,18]) linear_extrude(base_thickness) square(size=[3, 15], center=true);
            }
            
        }
        
        translate([25-14,55-base_thickness]) linear_extrude((50+base_thickness)/2) square(size=[28, base_thickness]);
            translate([25,55, 23+base_thickness]) rotate([90,0,0]) {
            linear_extrude(base_thickness) circle(d=28, $fn=fn);
        }
    }
    
    translate([25,55, 23+base_thickness]) rotate([90,0,0]) linear_extrude(base_thickness) circle(d=4, $fn=fn);
}