#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LINE_LEN 256
#define MAX_HEX_BYTES 32

int hexchar_to_int(char c) {
    return isdigit(c) ? c - '0' : tolower(c) - 'a' + 10;
}

int hexstr_to_bytes(const char *hex, unsigned char *bytes) {
    int len = strlen(hex);
    int i = 0, j = 0;

    if (len % 2 != 0) {
        bytes[0] = hexchar_to_int(hex[0]);
        i = 1;
        j = 1;
    }

    for (; i < len; i += 2, j++) {
        bytes[j] = (hexchar_to_int(hex[i]) << 4) | hexchar_to_int(hex[i + 1]);
    }

    return j;
}

int simulate_double(const unsigned char *input, int in_len, unsigned char *output) {
    int carry = 0;
    int out_len = in_len;
    for (int i = in_len - 1; i >= 0; i--) {
        int result = (input[i] << 1) + carry;
        output[i] = result & 0xFF;
        carry = (result >> 8) & 1;
    }

    if (carry) {
        memmove(output + 1, output, out_len);
        output[0] = 1;
        out_len += 1;
    }

    return out_len;
}

int compare_within_one(const unsigned char *a, const unsigned char *b, int len) {
    for (int i = 0; i < len; i++) {
        int diff = a[i] - b[i];
        if (diff < -1 || diff > 1)
            return 0;
    }
    return 1;
}

void print_hex(const unsigned char *bytes, int len) {
    int leading = 1;
    for (int i = 0; i < len; i++) {
        if (leading && bytes[i] == 0) continue;
        leading = 0;
        printf("%02x", bytes[i]);
    }
    if (leading) printf("00");
}

void check_mismatches(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Cannot open file");
        return;
    }

    char line[MAX_LINE_LEN];
    int line_num = 0;

    while (fgets(line, sizeof(line), file)) {
        line_num++;

        // Locate "Expected" and "Got"
        char *expected_ptr = strstr(line, "Expected ");
        char *got_ptr = strstr(line, "Got ");
        if (!expected_ptr || !got_ptr) continue;

        expected_ptr += 9; // Skip "Expected "
        got_ptr += 4;      // Skip "Got "

        // Extract hex strings
        char expected_hex[65], got_hex[65];
        sscanf(expected_ptr, "%64[0-9a-fA-F]", expected_hex);
        sscanf(got_ptr, "%64[0-9a-fA-F]", got_hex);

        unsigned char expected_bytes[MAX_HEX_BYTES], got_bytes[MAX_HEX_BYTES];
        int expected_len = hexstr_to_bytes(expected_hex, expected_bytes);
        int got_len = hexstr_to_bytes(got_hex, got_bytes);

        unsigned char simulated[MAX_HEX_BYTES + 1];
        int sim_len = simulate_double(expected_bytes, expected_len, simulated);

        int max_len = sim_len > got_len ? sim_len : got_len;
        unsigned char sim_aligned[MAX_HEX_BYTES + 1] = {0};
        unsigned char got_aligned[MAX_HEX_BYTES + 1] = {0};

        memcpy(sim_aligned + (max_len - sim_len), simulated, sim_len);
        memcpy(got_aligned + (max_len - got_len), got_bytes, got_len);

        printf("[Line %d] ", line_num);
        if (compare_within_one(sim_aligned, got_aligned, max_len)) {
            printf("✅ Approx match: 2*%s = ", expected_hex);
            print_hex(sim_aligned, max_len);
            printf(" ≈ %s\n", got_hex);
        } else {
            printf("❌ No match:     2*%s = ", expected_hex);
            print_hex(sim_aligned, max_len);
            printf(" ≠ %s\n", got_hex);
        }
    }

    fclose(file);
}

int main() {
    check_mismatches("new 5.txt");
    return 0;
}

