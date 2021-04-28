

/* Very basic logging class */

class Logging {

    debug(msg) {
        console.log(Date().toString() + " DEBUG " + msg);
    }

}

export default new Logging();
