class BlockEncoderDecoder:
    def __init__(self, max_blocks=100, max_coord_value=1000, block_type_range=10):
        """
        Initialize the encoder-decoder with the given constraints.
        :param max_blocks: Maximum number of blocks to encode.
        :param max_coord_value: Maximum value for each coordinate.
        :param block_type_range: Range of block types.
        """
        self.max_blocks = max_blocks
        self.max_coord_value = int(max_coord_value)
        self.block_type_range = int(block_type_range)
        self.coord_bits = self.max_coord_value.bit_length()
        self.block_type_bits = self.block_type_range.bit_length()
        self.block_bits = 3 * self.coord_bits + self.block_type_bits
        self.total_bits = self.block_bits * max_blocks

    def encode(self, block_positions):
        """
        Encode the block positions and types into a single integer.
        :param block_positions: List of tuples (x, y, z, block_type).
        :return: Encoded integer.
        """
        result = 0
        for idx, (x, y, z, block_type) in enumerate(block_positions):
            if not (0 <= x < self.max_coord_value and
                    0 <= y < self.max_coord_value and
                    0 <= z < self.max_coord_value and
                    1 <= block_type <= self.block_type_range):
                raise ValueError("Invalid block position or type")

            block_value = (x << (2 * self.coord_bits + self.block_type_bits)) | \
                          (y << (self.coord_bits + self.block_type_bits)) | \
                          (z << self.block_type_bits) | \
                          (block_type - 1)

            result |= block_value << (idx * self.block_bits)

        return result

    def decode(self, encoded_value):
        """
        Decode the encoded integer back into the original block positions and types.
        :param encoded_value: Encoded integer.
        :return: List of tuples (x, y, z, block_type).
        """
        block_positions = []
        for idx in range(self.max_blocks):
            shift_amount = idx * self.block_bits
            block_value = (encoded_value >> shift_amount) & ((1 << self.block_bits) - 1)

            if block_value == 0:
                break

            x = (block_value >> (2 * self.coord_bits + self.block_type_bits)) & ((1 << self.coord_bits) - 1)
            y = (block_value >> (self.coord_bits + self.block_type_bits)) & ((1 << self.coord_bits) - 1)
            z = (block_value >> self.block_type_bits) & ((1 << self.coord_bits) - 1)
            block_type = (block_value & ((1 << self.block_type_bits) - 1)) + 1

            block_positions.append((x, y, z, block_type))

        return block_positions


# Example usage
encoder_decoder = BlockEncoderDecoder(max_blocks=10, max_coord_value=1000, block_type_range=10)

# Example block positions (x, y, z, block_type)
block_positions = [
    (10, 20, 30, 1),
    (40, 50, 60, 2),
    (70, 80, 90, 3)
]

# Encode the block positions
encoded_value = encoder_decoder.encode(block_positions)
print(f"Encoded Value: {encoded_value}")

# Decode the encoded value
decoded_positions = encoder_decoder.decode(encoded_value)
print(f"Decoded Positions: {decoded_positions}")
