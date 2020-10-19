



motherboard($fn=60);


module motherboard() {
    difference() {
        square([210,100], true);
        /*polygon([
            [-210/2, 100/2],
            [-210/2, -100/2+29],
            [-210/2+67, -100/2+29],
            [-210/2+67, -100/2],
            [210/2, -100/2],
            [210/2, 100/2],
        ]);*/
                
        translate([-75,12]) rotate([0,0,-90]) scale([1,-1,1]) rpi();
        translate([15,-5]) rotate([0,0,90]) motor_esc();
        //translate([70, 25]) rotate([0,0,0]) audio_amp();
        //translate([70, -25]) rotate([0,0,0]) audio_amp();
        translate([-25,25]) rotate([0,0,0]) rtc();
        
        // Interface connectors
        translate([0,-45]) {
            translate([-30, 0]) pinheader(5, 5.12, center=true); // Power in           
            translate([5, 0]) pinheader(3, 5.12, center=true); // Motor out
            translate([25, 0]) pinheader(5, 2.56, center=true); // Motor Enc in
            translate([70, 0]) pinheader(4, 5.12, center=true); // Audio out
        }
    }
}


module motor_esc() {
    hl=57/2;
    hw=42/2;
    for (p=[[hl,hw], [hl,-hw], [-hl,-hw], [-hl,hw]]) translate(p) circle(d=3);
    
    translate([0,0]) square([52, (hw+2)*2], true);
    
    translate([hl+1,hw-5]) rotate([0,0,-90]) pinheader(5);
    translate([hl+1,-hw+5]) rotate([0,0,90]) pinheader(5);
    translate([-hl, 0]) rotate([0,0,90]) pinheader(5, 3.5, center=true);
}


module audio_amp() {
    hl=48.5/2;
    hw=28/2;
    for (p=[[hl,hw], [hl,-hw], [-hl,-hw], [-hl,hw]]) translate(p) circle(d=3);
    //square([hl*2-6, hw*2+3], true);
    translate([hl+1,hw-5]) rotate([0,0,-90]) pinheader(2, 12.5, center=true);

    
}


module fan(size=40) {
    circle(d=size-2);
    hs=size/2 - 4;
    for (p=[[hs,hs], [hs,-hs], [-hs,-hs], [-hs,hs]]) translate(p) circle(d=3);
}


module rpi(fan=true) {
    hl=58/2;
    hw=49/2;
    for (p=[[hl,hw], [hl,-hw], [-hl,-hw], [-hl,hw]]) translate(p) circle(d=3);   
    translate([85/2-10,-30]) square([30, 60]);
    
    translate([0,hw+2.56/2]) pinheader(20, center=true);
    translate([0,hw-2.56/2]) pinheader(20, center=true);
    
    if (fan) translate([(-hl-3.5)+29,(hw+3.5)-26]) fan(40);
}


module rtc() {
    translate([0,34/2]) pinheader(6, center=true);
    translate([0,-34/2])pinheader(4, center=true);
}





module pinheader(n=1, spacing=2.56, center=false) {
    translate([-((n-1)*spacing/2)*bool2int(center), 0]) {
        for (i=[0:1:n-1]) translate([i*spacing, 0]) circle(d=1);
    }
}

function bool2int(state) = state ? 1 : 0;