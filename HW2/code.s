	.file	"code.c"
	.text
	.globl	baz
	.type	baz, @function
baz:
	pushl	%ebp						; push %ebp into the stack
	movl	%esp, %ebp					; %ebp = %esp
	subl	$16, %esp					; %esp = %esp - 16; make space for 16 bytes on the stack
	movl	$0, -4(%ebp)				; (%ebp - 4) = 0; i is at %ebp - 4
	jmp	.L2
.L3:
	movl	-4(%ebp), %eax				; %eax = (%ebp - 4); %eax = i
	leal	0(,%eax,4), %edx			; %edx = %eax * 4; %edx = i * 4
	movl	8(%ebp), %eax				; %eax = %ebp + 8; %eax = vector
	addl	%eax, %edx					; %edx = %eax + %edx; %edx = vector + i * 4
	movl	16(%ebp), %eax				; %eax = %ebp + 16; %eax = value
	movl	%eax, (%edx)				; %edx = %eax; vector[i] = %eax (value)
	addl	$1, -4(%ebp)				; (%ebp - 4) = (%ebp - 4) + 1; i = i + 1
.L2:
	movl	-4(%ebp), %eax				; %eax = %ebp - 4; %eax = i
	cmpl	12(%ebp), %eax				; compare %eax with %ebp + 12; compare i with parameter len
	jl	.L3
	movl	12(%ebp), %eax
	leave
	ret
	.size	baz, .-baz
	.section	.rodata
.LC0:
	.string	"Sum is %d\n"
	.text
	.globl	main
	.type	main, @function
main:
	leal	4(%esp), %ecx				; %ecx = 4 + %esp
	andl	$-16, %esp					; %esp = %esp & -16
	pushl	-4(%ecx)					; push %ecx - 4 into the stack
	pushl	%ebp						; push %ebp into the stack
	movl	%esp, %ebp					; %ebp = %esp
	pushl	%ecx						; push %ecx into the stack; standard setup until this pointc
	subl	$84, %esp					; %esp = %esp - 84; make space for 84 (21 steps) bytes on the stack
	pushl	$16							; push the integer 16 into the stack; parameter 16 pushed into the stack
	pushl	$16							; push the integer 16 into the stack; parameter BUFSIZE pushed into the stack
	leal	-84(%ebp), %eax				; %eax = %ebp - 84
	pushl	%eax						; push %eax into the stack; parameter buffer pushed into the stack
	call	baz							; call baz
	addl	$12, %esp					; %esp = %esp + 12
	movl	%eax, -20(%ebp)				; %eax = %ebp - 20; x is at %ebp - 20
	movl	$0, -16(%ebp)				; %ebp - 16 = 0; sum is at %ebp - 16
	movl	$0, -12(%ebp)				; %ebp - 12 = 0; i is at %ebp - 12
	jmp	.L6
.L7:
	movl	-12(%ebp), %eax
	movl	-84(%ebp,%eax,4), %eax		; %eax = *((%ebp + %eax * 4) - 84); eax = buffer[i]
	addl	%eax, -16(%ebp)				; %eax = %eax + %ebp - 16; sum = sum + buffer[i]
	addl	$1, -12(%ebp)				; %ebp - 12 = %ebp - 12 + 1; i = i + 1
.L6:
	cmpl	$15, -12(%ebp)
	jle	.L7
	subl	$8, %esp
	pushl	-16(%ebp)
	pushl	$.LC0
	call	printf
	addl	$16, %esp
	movl	$0, %eax
	movl	-4(%ebp), %ecx
	leave
	leal	-4(%ecx), %esp
	ret
	.size	main, .-main
	.ident	"GCC: (GNU) 12.2.0"
	.section	.note.GNU-stack,"",@progbits
