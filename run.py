# run.py
from app.main import TextSummarizerApp
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='Text Summarizer with Sentiment Analysis')
    parser.add_argument('input', help='Input text or file path')
    parser.add_argument('--mode', choices=['extractive', 'abstractive', 'hybrid'], 
                       default='hybrid', help='Summarization mode')
    parser.add_argument('--sentences', type=int, default=3, 
                       help='Number of sentences for extractive summary')
    parser.add_argument('--output', help='Output file path (JSON format)')
    
    args = parser.parse_args()
    
    app = TextSummarizerApp(mode=args.mode)
    
    try:
        # Check if input is a file
        with open(args.input, 'r') as f:
            text = f.read()
    except (FileNotFoundError, OSError):
        # Treat input as text
        text = args.input
    
    report = app.generate_report(text, args.sentences)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {args.output}")
    else:
        print("\n=== Summary ===")
        print(report['summary'])
        print("\n=== Tone Analysis ===")
        print(f"Sentiment: {report['sentiment']} ({report['confidence']:.2f})")
        print(f"Tone: {report['tone']}")
        print(f"\nLength reduced from {report['original_length']} to {report['summary_length']} words")

if __name__ == '__main__':
    main()