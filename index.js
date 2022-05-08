function innerProduct(vec_a, vec_b) {
    /*
    Calculate inner product of two vecter, vec_a and vec_b.
    */
   let ret = 0
   if (vec_a.length == vec_b.length) {
        for (let i=0; i<vec_a.length; i++) {
            ret += vec_a[i] * vec_b[i];
        }
   }
   return ret;
}

function regression(x, y) {
    /*
    Curve fitting of form y=a*sin(x+b), where a is positive and b is in [0, 2*pi).
    It uses angle addition formula and bilinear least-square method.

    Let A = a cos(b), B = a sin(b), Si = sin(xi) and Ci = cos(xi)
    y = a sin(x+b) = a cos(b)sin(x) +  sin(b)cos(x) = A*Si + B*Ci.
    Here, the bilinear model y = f(S,C) = AS + BC can be obtained.
    */
    const [S, C] = [x.map(Math.sin), x.map(Math.cos)];
    
    const d = innerProduct(S, S) * innerProduct(C, C) - innerProduct(S, C) * innerProduct(S, C);
    const A = (innerProduct(y, S) * innerProduct(C, C) - innerProduct(S, C) * innerProduct(y, C)) / d;
    const B = (innerProduct(S, S) * innerProduct(y, C) - innerProduct(y, S) * innerProduct(S, C)) / d;
    let [a, b] = [Math.sqrt(A**2 + B**2), Math.atan(B/A)];
    let [posErr, negErr] = [0, 0];
    for (let i=0; i<x.length; i++) {
        posErr += (y[i] - a * Math.sin(x[i]+b)) ** 2;
        negErr += (y[i] + a * Math.sin(x[i]+b)) ** 2;
    }
    a = posErr <= negErr ? a : -a;
    return [a, b];
}
