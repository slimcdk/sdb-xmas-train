


fn = 30;
base_thickness = 2;

bolt_d = 3;
standoff_height = 6;



difference() {
    linear_extrude(base_thickness) square(size=[133,170]);
    
    translate([105,90,0]) rotate([0,0,90]) union() {

        translate([-71,0,0]) linear_extrude(base_thickness+1) circle(d=4, $fn=fn);
        translate([71,0,0]) linear_extrude(base_thickness+1) circle(d=4, $fn=fn);
    }

    translate([20,115,0]) rotate([0,0,90]) union() {

        translate([-7,0,0]) linear_extrude(base_thickness+1) circle(d=3, $fn=fn);
        translate([7,0,0]) linear_extrude(base_thickness+1) circle(d=3, $fn=fn);
    }
    
    #translate([85,167,1]) rotate([0,0,-90]) linear_extrude(1) {
        text("Christian Skjerning", size=5.5);
    }
    #translate([78,167,1]) rotate([0,0,-90]) linear_extrude(1) {
        text("November 2019", size=5.5);
    }
    
}


// raspberry pi
translate([28, 102, base_thickness]) rotate([0,0,-90]) union () {
    
    // standoffs
    standoff_spacing = [49, 58];
    
    // standoff 1
    translate([0, 0, 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 2
    translate([standoff_spacing[0], 0, 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 3
    translate([0, standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 4
    translate([standoff_spacing[0], standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
}

// buck converter
translate([107, 55, base_thickness]) rotate([0,0,0]) union () {
    
    
    // standoffs
    standoff_spacing = [18, 36];
           
    // standoff 1
    translate([0, 0, 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 2
    translate([standoff_spacing[0], standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
}



// motor
translate([63,128, base_thickness]) rotate([0,0,90]) union () {       
    
    // standoffs
    standoff_spacing = [36, 57.5];
          
    // standoff 1
    translate([0,0,0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 2
    translate([standoff_spacing[0], 0, 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 3
    translate([0, standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 4
    translate([standoff_spacing[0], standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    
}


// arduino base
translate([110, 116, base_thickness]) rotate([0,0,0]) union () {
    
   
    standoff_spacing = [0, 40];
 
    // standoff 1
    translate([0, 0, 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 2
    translate([0, standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);   
    }
}


// amplifier 1 base
translate([55, 6, base_thickness]) rotate([0,0,90]) union () {
    
    standoff_spacing = [27.5, 48];
        
    // standoff 1
    translate([0, 0, 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 2
    translate([standoff_spacing[0], 0, 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 3
    translate([0, standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 4
    translate([standoff_spacing[0], standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    
}



// amplifier 2 base
translate([125, 6, base_thickness]) rotate([0,0,90]) union () {
    
    
    standoff_spacing = [27.5, 48];
        
    // standoff 1
    translate([0, 0, 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 2
    translate([standoff_spacing[0], 0, 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 3
    translate([0, standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
    // standoff 4
    translate([standoff_spacing[0], standoff_spacing[1], 0]) difference() {
        linear_extrude(standoff_height) circle(d=bolt_d+3, $fn=fn);
        linear_extrude(standoff_height) circle(d=bolt_d, $fn=fn);
    }
}