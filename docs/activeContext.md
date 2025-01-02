# Active Context

## Current Work
- Implementing token calculation logic based on TypeScript reference
- Updating pip package with new functionality
- Ensuring tests cover new implementations

## Recent Changes
1. Updated calculator.py with new token calculation logic
   - Added TokenResult named tuple for structured returns
   - Implemented warnings for large images
   - No automatic resizing, preserving original dimensions

2. Updated README.md
   - Added documentation about image size handling
   - Included examples of return values
   - Added warnings and optimization suggestions

3. Package Updates
   - Version bumped to 0.1.2a1
   - Updated setup.py and __init__.py
   - Rebuilt and uploaded to PyPI

## Next Steps
1. **Testing**
   - Add comprehensive unit tests for new functionality
   - Test edge cases and error handling
   - Verify token calculations against reference implementation

2. **Documentation**
   - Add detailed API reference
   - Include more usage examples
   - Document warning messages and their meanings

3. **Optimization**
   - Profile performance
   - Optimize memory usage
   - Improve batch processing efficiency

4. **Future Features**
   - Add support for more models
   - Implement caching
   - Add async support for batch operations 