
PCB_LAYERS = [
    ["yellow", "production-files/motherboard-Edge_Cuts.svg"],
    ["red", "production-files/motherboard-F_Adhes.svg"],
    ["red", "production-files/motherboard-F_Cu.svg"],
    ["red", "production-files/motherboard-F_Mask.svg"],
    ["red", "production-files/motherboard-F_Paste.svg"],
    ["red", "production-files/motherboard-F_SilkS.svg"],   
    //"production-files/motherboard-B_Adhes.svg",
    //"production-files/motherboard-B_Cu.svg",
    //"production-files/motherboard-B_Mask.svg",
    //"production-files/motherboard-B_Paste.svg",
    //"production-files/motherboard-B_SilkS.svg",
];

o = 2.5;
pcb_mounting_holes = [[0, 42], [-67, 42], [-92, 22], [-91.5,-39], [-28.5,-79], [76.5,-79], [76.5,-28.75], [76.5,21.5], [67, 42]];
fan_size = 40;
fhs=fan_size/2-4;
fan_shroud_holes = [[-60,-6], [22,18]/*, [5,-60]*/];
fan_mounting_holes = [for (fs=fan_shroud_holes) for (p=[[fhs,fhs], [fhs,-fhs], [-fhs,-fhs], [-fhs,fhs]]) fs+p];


// Assembly
translate([0,-205/2]) rotate([0,0,180]) {
    translate([0,-30+2,12]) color("gray") psu($fn=60);
    color("yellow") psu_mount($fn=60);
}

translate([0,205/2]) {
    translate([0,0,10+13]) color("green") /*!projection()*/ motherboard(layers_dir="production-files/", use_layers=false, $fn=60);
    color("yellow") !mb_mount($fn=100);
    color("beige") for (p=fan_shroud_holes) translate([p[0],p[1],11]) fan_body($fn=60);
}


function bool2int(state) = state ? 1 : 0;



module motherboard(layers_dir, use_layers=false) {
    
    pts = [
        // First corner
        [-70,45],
        [-70, 45-20],
        [-75-20, 45-20],
     
        // Second corner
        [-75-20, -42],
        [-32, -42],
        [-32, -50-32],
    
        // Third corner
        [80, -50-32],
    
        // Forth corner
        [80, 45-20],
        [70, 45-20],
        [70, 45]
    ];
    

    linear_extrude(1.6) difference() {
        polygon(pts);
        for (p=pcb_mounting_holes) translate(p) circle(d=3);
        for (p=fan_mounting_holes) translate(p) circle(d=4);
        for (p=fan_shroud_holes) translate(p) circle(d=fan_size-2);
        //for (p=fan_shroud_holes) translate(p) square([fan_size+1, fan_size+1], true);


        // Modules
        translate([-60,-10]) rotate([0,0,-90]) mirror([0,1,0]) rpi(fan=false);
        translate([18,18]) rotate([0,0,-180]) motor_esc(debug=false);
        translate([-45,34]) rotate([0,0,90]) rtc(debug=false);      
    }
    
    
    if (use_layers) translate([-180, -147, 1.6]) linear_extrude(0.01) color("red") import(str(layers_dir, "motherboard-F_Cu.svg"));
    if (use_layers) translate([-180, -147, -0.01]) linear_extrude(0.01) color("black") import(str(layers_dir, "motherboard-B_Cu.svg"));
}


module motor_esc(debug=false) {
    hl=57/2;
    hw=36.5/2;
    for (p=[[hl,hw], [hl,-hw], [-hl,-hw], [-hl,hw]]) translate(p) circle(d=3);
    if (debug) square([64,43], true);
    *translate([2.5,0]) square([hl*2-10, (hw)*2], true);
    
    translate([hl+.5, 0]) {
        translate([0,hw-4]) rotate([0,0,-90]) pinheader(6);
        translate([0,-hw+3]) rotate([0,0,90]) pinheader(5);
    }
    translate([-hl+1, 2-10]) rotate([0,0,90]) pinheader(5, 4, center=false);
}


module audio_amp() {
    hl=48.5/2;
    hw=28/2;
    for (p=[[hl,hw], [hl,-hw], [-hl,-hw], [-hl,hw]]) translate(p) circle(d=3);
    //square([hl*2-6, hw*2+3], true);
    translate([hl+1,hw-5]) rotate([0,0,-90]) pinheader(2, 12.5, center=true);
}

module fan_body() {
    linear_extrude(13) difference() {
        square([fan_size,fan_size], true);
        fan_holes();
    }
}

module fan_holes() {
    circle(d=fan_size-2);
    hs=fan_size/2 - 4;
    for (p=[[hs,hs], [hs,-hs], [-hs,-hs], [-hs,hs]]) translate(p) circle(d=3);
}


module rpi(fan=true, debug=false) {
    hl=58/2;
    hw=49/2;
    for (p=[[hl,hw], [hl,-hw], [-hl,-hw], [-hl,hw]]) translate(p) circle(d=3);   
    translate([32+40/2,0]) square([40, 56], center=true);
    
    translate([0,hw+2.56/2]) pinheader(20, 2.54, center=true);
    translate([0,hw-2.56/2]) pinheader(20, 2.54, center=true);
    
    if (fan) translate([-hl+3.5+20.75,hw+3.5-26]) fan_holes(40);
}


module rtc(debug=false) {
    translate([0,34/2]) pinheader(6, center=true);
    translate([0,-34/2])pinheader(4, center=true);
    if(debug) square([22,37], center=true);
}


module pinheader(n=1, spacing=2.54, center=false) {
    translate([-((n-1)*spacing/2)*bool2int(center), 0]) {
        for (i=[0:1:n-1]) translate([i*spacing, 0]) circle(d=1);
    }
}





module mb_mount() {
    pts = [
        // First corner
        [-70,45],
        [-70, 45-20],
        [-75-20, 45-20],
    
        // Second corner
        [-75-20, -50-35],
    
        // Third corner
        [60+20, -50-35],
    
        // Forth corner
        [60+20, 45-20],
        [70, 45-20],
        [70, 45]
    ]; 
    
    linear_extrude(3) difference() {
        polygon(pts);
        for (p=[[140/2,0], [-140/2,0]]) translate(p) circle(d=8);
        translate([0,-20]) circle(d=110);
    }
    
    linear_extrude(10) for (p=[[140/2,0], [-140/2,0]]) translate(p) difference() {
        circle(d=12);
        circle(d=8);
    }
    
    *for (p=fan_mounting_holes) translate(p) linear_extrude(11) difference() {
        circle(d=6);
        circle(d=3);
    }

    for (p=pcb_mounting_holes) translate(p) linear_extrude(10+13) difference() {
        circle(d=6);
        circle(d=3);
    }
    
}




module psu() {
    
    linear_extrude(86) square([141, 151], true);
    for (p=[[140/2-5,150/2-15], [140/2-5,-150/2+20], [-140/2+7,-150/2+10], [-140/2+7,150/2-15]]) translate(p) rotate([180,0,0]) linear_extrude(3) circle(d=7);
    for (p=[-150/2+5, 150/2-5]) translate([-140/2,p, 5]) rotate([0,-90,0]) linear_extrude(5) { 
        circle(d=10);
        translate([86/2,0]) square([86,10], true);
    }
}


/// **** MOUNTING **** ///
module psu_mount() {
    pts = [
        // First corner
        [-70,45],
        [-70, 45-20],
        [-60-15, 45-20],
    
        // Second corner
        [-60-15, -108],
    
        // Third corner
        [60+15, -108],
    
        // Forth corner
        [60+15, 45-20],
        [70, 45-20],
        [70, 45]
    ]; 
    
    difference() {
        union() {
            linear_extrude(3) polygon(pts);
            linear_extrude(10) for (p=[[140/2,0], [-140/2,0]]) translate(p) circle(d=12);
            linear_extrude(30) for(p=[-60, 60+15]) translate([p, 25]) rotate([0,0,180]) square([15,128+5]);
        }
        linear_extrude(12) for (p=[[140/2,0], [-140/2,0]]) translate(p) circle(d=8);
        translate([0,-30+2,12]) psu();
        translate([0,-30]) linear_extrude(3) circle(d=110);
    }
}
